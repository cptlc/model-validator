"""
Copyright (c) 2016 Gabriel A. Weaver, Information Trust Institute
All rights reserved.

Developed by:             Gabriel A. Weaver, Information Trust Institute
                          University of Illinois at Urbana-Champaign
                          http://www.iti.illinois.edu/

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal with the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimers.
Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimers in the
documentation and/or other materials provided with the distribution.

Neither the names of Gabriel A. Weaver, Information Trust Institute,
University of Illinois at Urbana-Champaign, nor the names of its
contributors may be used to endorse or promote products derived from
this Software without specific prior written permission.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE
SOFTWARE.
"""
from jsonschema import Draft4Validator
import json
import logging
import os

class JSONValidator():
    """
    JSONValidator both checks the JSON Schema provided and
     validates the json files in a directory against that schema.
    """
    schema = None
    
    def check_schema(self):
        """
        Check the schema against Draft 4 of the JSON Schema Spec

        :return: returns -1 if there are schema errors, 0 on success
        """
        if (Draft4Validator.check_schema(self.schema)):
            return 0
        return -1

    def validate_file(self, json_data_file_path):
        """
        Validate the contents of the file against the schema

        :param json_data_file_path:  The path to the file to validate
        :return:  returns -1 if there are validation errors, 0 on success
        """
        json_data_file = open(json_data_file_path, 'r')
        json_data = json.load(json_data_file)
        json_data_file.close()
        
        v = Draft4Validator(self.schema)
        errors = sorted(v.iter_errors(json_data), key=lambda e: e.path)
        for error in errors:
            logging.warning(error.message)
            
        if len(errors) > 0:
            return -1

        return 0

    def validate_files(self, json_dir_path):
        """
        Validate all files with a .json suffix in the given directory
        
        :param json_dir_path:  The path to the directory
        :return:  returns -1 if there are validation errors, 0 on success. 
        """
        for file_path in os.listdir( json_dir_path ):
            if ( file_path.endswith(".json") ) :
                errorcode = self.validate_file( json_dir_path + "/" + file_path )
                if ( errorcode ):
                    logging.warning("Failed to validate: " + file_path + ".")
                    return -1
        return 0

    @staticmethod
    def create( schema_file_path ):
        """
        Create a JSON Validator for the schema provided

        :param schema_file_path:  The path to the schema
        :return:  returns an instance of the JSONValidator for the given schema
        """
        jv = JSONValidator()

        schema_file = open( schema_file_path, 'r' )
        jv.schema = json.load(schema_file)
        schema_file.close()
        return jv
