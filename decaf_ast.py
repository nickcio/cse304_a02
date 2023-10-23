import sys
import json

valid_types = ["int", "boolean", "string", "float", "double", "char"]
user_defined_types = []

def error(string):
  RED = '\033[91m'
  CLEAR_COLOR = '\033[0m'
  print(f"{RED}ERROR:{CLEAR_COLOR} {string}", file=sys.stderr)
  exit(1)

class AST:

    def _init_(self, ast, fields, methods, constructors):
        self.ast = ast
        self.fields = fields
        self.methods = methods
        self.constructors = constructors
        writeJSON("ast.json", ast)

        if "class_name" not in ast:
            error("Could not find class name")
        if ast["class_name"] == "":
            error("Class name is empty")
        self.class_name = ast["class_name"]

        if "superclass" not in ast:
            error("Could not find superclass name")
        self.superclass_name = ast["superclass"]

        global scope
        # Check if class name is already defined
        if self.class_name in scope["global"]:
            error(f"Line:{ast['line_num']}:{ast['col_num']}: Class name already defined")

        children = []
        def set_super_true(child):
          # get keys
          keys = list(child.keys())
          for key in keys:
            child[key]["super"] = True
          return child
        
        if self.superclass_name != "":
          children = scope["global"][self.superclass_name]["children"]
          children = [set_super_true(child) for child in children]

        self.scope = self.add_to_scope(scope["global"], [], self.class_name, {"type": "class", "superclass_name": self.superclass_name, "children": children, "id_num": class_count, "id": self.class_name,  "line_num": ast["line_num"], "col_num": ast["col_num"]})

        self.printed = self.create_record(self.ast, self.scope[self.class_name])
        scope["global"] = self.scope

    def print_ast(self):
        return self.printed
    
    def create_constructor_record(self, scope, scope_array):

        output = "Constructors:\n"
        for constructor_id in self.constructors.keys():
            local_scope = scope.copy()
            local_scope_array = scope_array.copy()
            constructor = self.constructors[constructor_id]

            if "modifiers" not in constructor:
                error(f"Line:{constructor['line_num']}:{constructor['col_num']}: Could not find constructor modifiers")
            constructor_modifiers = self.create_modifiers_list_PRIVATE_PUBLIC(
                constructor["modifiers"])

            output += f"CONSTRUCTOR: {constructor_id}, {constructor_modifiers}\n"
            output += "Constructor Parameters:\n"
            
            local_scope = self.add_to_scope(scope, scope_array, constructor_id, {"super": False, "type": "constructor", "id": self.class_name, "id_num": constructor_id, "modifiers": constructor["modifiers"] ,"children": [], "line_num": constructor["line_num"], "col_num": constructor["col_num"]})
            local_scope = self.traverse_scope_layer(local_scope, [constructor_id, "children"])
            local_scope_array.append(constructor_id)
            local_scope_array.append("children")


            output += "Variable Table:\n"
            for variable_id in constructor["formals"].keys():
                variable = constructor["formals"][variable_id]
                self.add_to_scope(local_scope, local_scope_array, variable["id"], {"super": False, "type": f"{self.create_type_record(variable['type'])}", "id_num": variable_id, "id": variable["id"], "formal": True, "var_type": "local", "line_num": variable["line_num"], "col_num": variable["col_num"]})
                output += self.create_variable_record(variable_id, variable)
                        
            block = self.create_block_record(constructor["body"], local_scope, local_scope_array)

            output += "Constructor Body:\n"
            output += block
        return output

    def create_record(self, ast, scope):
        output = ""
        global user_defined_types
        output += f"Class Name: {self.class_name}\n"
        user_defined_types.append(ast["class_name"])

        output += f"Superclass: {self.superclass_name}\n"

        # scope 
        scopeArray = ["global", self.class_name]

        # Check fields
        if "fields" not in ast["body"]:
            error("Could not find fields")
        self.fields = ast["body"]["fields"]
        output += self.create_field_record(scope["children"], scopeArray + ["children"])

        # check constructors
        if "constructors" not in ast["body"]:
            error("Could not find constructors")
        self.constructors = ast["body"]["constructors"]
        output += self.create_constructor_record(scope["children"], scopeArray + ["children"])

        if "methods" not in ast["body"]:
            error("Could not find methods")
        self.methods = ast["body"]["methods"]
        output += self.create_method_record(scope["children"], scopeArray + ["children"])
        return output
    

    def create_field_record(self, scope, scope_array):
        output = "Fields:\n"
        blacklist = []
        for field_id in self.fields.keys():
            field = self.fields[field_id]

            if "id" not in field:
                error(f"Line:{field['line_num']}:{field['col_num']}: Could not find field names (id)")

            field_name = field["id"]

            if "type" not in field:
                error(f"Line:{field['line_num']}:{field['col_num']}: Could not find field type")
            
            field_type = self.create_type_record(field["type"])
            
            if "modifiers" not in field:
                error(f"Line:{field['line_num']}:{field['col_num']}: Could not find field modifiers")
            
            field_modifiers = self.create_modifiers_list(field["modifiers"])
            var_object = {"super": False, "type": f"{field_type}","id": field_name, "formal": False, "var_type": "field","id_num": field_id, "modifiers": field["modifiers"], "line_num": field["line_num"], "col_num": field["col_num"]}
            self.add_to_scope(scope, scope_array, field_name,var_object)

            output += f"FIELD {field_id}, {field_name}, {self.class_name}, {field_modifiers}, {field_type}\n"
        return output
    
    def create_method_record(self, scope, scope_array):
        output = "Methods:\n"
        for method_id in self.methods.keys():
            local_scope = scope
            local_scope_array = scope_array.copy()
            method = self.methods[method_id]

            method_name = method["function_id"]

            method_modifiers = self.create_modifiers_list(method["modifiers"])

            method_type = self.create_type_record(method["type"], 1)

            output += f"METHOD: {method_id}, {method_name}, {self.class_name}, {method_modifiers}, {method_type}\n"
            output += "Method Parameters:\n"

            local_scope = self.add_to_scope(local_scope, local_scope_array, method_name, {"super": False, "type": "method", "id": method_id, "id_num": method_id, "modifiers": method["modifiers"], "return_type": method["type"], "children": [], "line_num": method["line_num"], "col_num": method["col_num"]})
            local_scope = self.traverse_scope_layer(local_scope, [method_name, "children"])
            local_scope_array.append(method_name)
            local_scope_array.append("children")

            for variable_id in method["formals"].keys():
                variable = method["formals"][variable_id]
                self.add_to_scope(local_scope, local_scope_array, variable["id"], {"super": False, "type": f"{self.create_type_record(variable['type'])}", "id_num": variable_id, "id": variable["id"], "var_type": "local", "formal": True,"line_num": variable["line_num"], "col_num": variable["col_num"] })
                output += self.create_variable_record(variable_id, variable)

            block = self.create_block_record(method["body"], local_scope, local_scope_array)
            
            output += "Variable Table:\n"

            for variable in local_scope:
              for var_id in variable.keys():
                if variable[var_id]["formal"]:
                  continue
                output += self.create_variable_record(variable[var_id]["id_num"], variable[var_id])

            output += "Method Body:\n"
            output += block
        return output
    
    def create_type_record(self, ast_type, return_type=0):
      
        output = ""
        global valid_types, user_defined_types

        local_valid_types = valid_types.copy()
        if return_type == 1:
            local_valid_types.append("void")

        if ast_type in user_defined_types:
            output += f"user({ast_type})"
            return output

        if ast_type not in local_valid_types:
            error(f"Line:{ast_type['line_num']}:{ast_type['col_num']}: Invalid type {ast_type}")
        
        output += f"{ast_type}"
        return output
    
    def create_variable_record(self, variable_id, ast_variable):
        output = ""
        output += f"VARIABLE {variable_id}, {ast_variable['id']}, {ast_variable['var_type']}, {ast_variable['type']}\n"
        return output
    
    def create_modifiers_list(self, ast_modifiers):
        output = "private"
        if ast_modifiers == []:
            output = "private, instance"
        elif ast_modifiers == ["public"]:
            output = "public, instance"
        elif ast_modifiers == ["static"]:
            output = "private, static"
        elif ast_modifiers == ["public", "static"]:
            output = "public, static"
        elif ast_modifiers == ["private", "static"]:
            output = "private, static"
        return output
    
    def create_modifiers_list_PRIVATE_PUBLIC(self, ast_modifiers):
        output = ""
        if ast_modifiers == []:
            output = "private"
        elif "private" in ast_modifiers:
            output = "private"
        else:
            output = "public"
        return output
    
# print ast

def print_ast_blocks(ast_blocks):
    big_asm = ""
    output = "-----------------------------------------------\n"
    for ast in ast_blocks:
        if ast == None:
            continue
        out, asm = ast.print_ast()
        output += out
        big_asm += asm
        output += "-----------------------------------------------\n"
    global static_count
    big_asm = f".static_data {static_count}\n{big_asm}"
    return output, big_asm



    
# extraction functions

def extract_body(ast):
    if "body" not in ast:
        raise Exception("Could not find body")
    global field_count, method_count, class_count, class_overall_count
    ast["id_num"] = class_overall_count
    class_overall_count += 1
    fields = {}
    methods = {}
    constructors = {}
    for item in ast["body"]:
        if 'field' in item:
          for id_name in item['field']['ids']:
              fields[field_count] = item['field']
              fields[field_count]['id'] = id_name
              del fields[field_count]['ids']
              field_count += 1
        elif 'method' in item:
            methods[method_count] = item['method']
            method_count += 1
        elif 'constructor' in item:
            constructors[class_count] = item['constructor']
            class_count += 1
        else:
            # raise Exception("Could not find field, method, or constructor")
            error(f"Could not find field, method, or constructor at line:{['line_num']}:{['col_num']}")
    ast["body"] = {"fields": fields, "methods": methods,
                   "constructors": constructors}
    return AST(ast, fields, methods, constructors)


def extract_variables_from_formals(key, ast):
    if key not in ast:
        raise Exception(f"Could not find {key}")
    if 'formals' not in ast[key]:
        raise Exception("Could not find formals")
    global var_count
    params = {}
    for item in ast[key]["formals"]:
        if 'parameter' in item:
            item['parameter']['var_type'] = 'local'
            params[var_count] = item['parameter']
            var_count += 1
        else:
            raise Exception("Could not find variable")
    ast[key]["formals"] = params
    return ast


def extract_variables_from_field(ast):
    if 'field' not in ast:
        raise Exception("Could not find field")
    if 'variables' not in ast['field']:
        raise Exception("Could not find variables")
    if 'type' not in ast['field']['variables']:
        raise Exception("Could not find type")
    if 'ids' not in ast['field']['variables']:
        raise Exception("Could not find ids")
    ast['field']['type'] = ast['field']['variables']['type']
    ast['field']['ids'] = ast['field']['variables']['ids']
    ast['field']['col_num'] = ast['field']['variables']['col_num']
    ast['field']['line_num'] = ast['field']['variables']['line_num']
    del ast['field']['variables']
    return ast

def compare_var(obj1,obj2):
  if obj1 == obj2:
    return True
  if isinstance(obj1, dict) and isinstance(obj2, dict):
    if "type" not in obj1 or "type" not in obj2:
      return False
    if obj1["type"] != obj2["type"]:
      return False
    if "id" not in obj1 or "id" not in obj2:
      return False
    if obj1["id"] != obj2["id"]:
      return False
    if "var_type" not in obj1 or "var_type" not in obj2:
      return False
    if obj1["var_type"] != obj2["var_type"]:
      return False
    return True
  return False

# printing functions

def writeJSON(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent=2)
    return True

def readJSON(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data


def writeAST(ast_blocks):
    global scope

    return print_ast_blocks(ast_blocks)

def print_ast_blocks(ast_blocks):
    output = "-----------------------------------------------\n"
    for ast in ast_blocks:
        if ast == None:
            continue
        output += ast.print_ast()
        output += "-----------------------------------------------\n"
    return output