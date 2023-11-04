# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

import json, sys

field_count = 1
method_count = 6
class_count = 1
class_overall_count = 3
var_count = 1
valid_types = ["int", "boolean", "string", "float", "double", "char"]
user_defined_types = []

in_class = {
    "type": "class",
    "id_num": 1,
    "children": [
        {
            "scan_int": {
                "type": "method",
                "id_num": 1,
                "return_type": "int",
                "modifiers": ["public", "static"],
                "children": {},
            }
        },
        {
            "scan_float": {
                "type": "method",
                "id_num": 2,
                "return_type": "float",
                "modifiers": ["public", "static"],
                "children": {},
            }
        },
    ],
}

out_class = {
    "type": "class",
    "id_num": 2,
    "children": [
        {
            "print": {
                "type": "method",
                "id_num": 3,
                "return_type": "void",
                "modifiers": ["public", "static"],
                "children": [
                    {
                        "i": {
                            "type": "int",
                            "var_type": "field",
                            "id_num": 2,
                            "return_type": "string",
                            "children": {},
                        }
                    }
                ],
            }
        },
        {
            "print": {
                "type": "method",
                "id_num": 1,
                "modifiers": ["public", "static"],
                "return_type": "void",
                "children": [
                    {
                        "i": {
                            "type": "float",
                            "id_num": 1,
                            "id": "i",
                            "var_type": "formal",
                        }
                    }
                ],
            }
        },
        {
            "print": {
                "type": "method",
                "id_num": 1,
                "modifiers": ["public", "static"],
                "return_type": "void",
                "children": [
                    {
                        "i": {
                            "type": "string",
                            "id_num": 1,
                            "id": "i",
                            "var_type": "formal",
                        }
                    }
                ],
            }
        },
        {
            "print": {
                "type": "method",
                "id_num": 6,
                "modifiers": ["public", "static"],
                "return_type": "void",
                "children": [
                    {
                        "i": {
                            "type": "boolean",
                            "id_num": 1,
                            "id": "i",
                            "var_type": "formal",
                        }
                    }
                ],
            }
        },
    ],
}

scope = {"global": {"In": in_class, "Out": out_class}}


class err_class(Exception):
    def __init__(self, msg):
        self.msg = msg
        RED = "\033[91m"
        CLEAR_FORMAT = "\033[0m"
        self.err_msg = f"{RED}ERROR: {CLEAR_FORMAT}{msg}"
        raise Exception(self.err_msg)

    def __str__(self):
        return self.msg


def warn(string):
    YELLOW = "\033[93mWARN: "
    CLEAR_COLOR = "\033[0m"
    print(YELLOW + str(string) + CLEAR_COLOR)


def error(string):
    RED = "\033[91m"
    CLEAR_COLOR = "\033[0m"
    print(f"{RED}ERROR:{CLEAR_COLOR} {string}", file=sys.stderr)
    exit(1)


class AST:
    def __init__(self, ast, fields, methods, constructors):
        self.ast = ast
        self.fields = fields
        self.methods = methods
        self.constructors = constructors

        if "class_name" not in ast:
            error("Could not find class name")
        if ast["class_name"] == "":
            error("Class name is empty")
        self.class_name = ast["class_name"]

        if "superclass" not in ast:
            error("Could not find superclass name")
        self.superclass_name = ast["superclass"]

        global scope
        if self.class_name in scope["global"]:
            error(
                f"Line:{ast['line_num']}:{ast['col_num']}: Class name already defined"
            )

        children = []

        def set_super_true(child):
            keys = list(child.keys())
            for key in keys:
                child[key]["super"] = True
            return child

        if self.superclass_name != "":
            children = scope["global"][self.superclass_name]["children"]
            children = [set_super_true(child) for child in children]

        self.scope = self.add_to_scope(
            scope["global"],
            [],
            self.class_name,
            {
                "type": "class",
                "superclass_name": self.superclass_name,
                "children": children,
                "id_num": class_count,
                "id": self.class_name,
                "line_num": ast["line_num"],
                "col_num": ast["col_num"],
            },
        )

        self.printed = self.create_record(self.ast, self.scope[self.class_name])
        scope["global"] = self.scope

    def print_ast(self):
        return self.printed

    def create_record(self, ast, scope):
        output = ""
        global user_defined_types
        output += f"Class Name: {self.class_name}\n"
        user_defined_types.append(ast["class_name"])

        output += f"Superclass: {self.superclass_name}\n"

        scope_array = ["global", self.class_name]

        if "fields" not in ast["body"]:
            error("Could not find fields")
        self.fields = ast["body"]["fields"]
        output += self.create_field_record(
            scope["children"], scope_array + ["children"]
        )

        if "constructors" not in ast["body"]:
            error("Could not find constructors")
        self.constructors = ast["body"]["constructors"]
        output += self.create_constructor_record(
            scope["children"], scope_array + ["children"]
        )

        if "methods" not in ast["body"]:
            error("Could not find methods")
        self.methods = ast["body"]["methods"]
        output += self.create_method_record(
            scope["children"], scope_array + ["children"]
        )
        return output

    def create_field_record(self, scope, scope_array):
        output = "Fields:\n"
        blacklist = []
        for field_id in self.fields.keys():
            field = self.fields[field_id]

            if "id" not in field:
                error(
                    f"Line:{field['line_num']}:{field['col_num']}: Could not find field names (id)"
                )
            field_name = field["id"]
            if "type" not in field:
                error(
                    f"Line:{field['line_num']}:{field['col_num']}: Could not find field type"
                )
            field_type = self.create_type_record(field["type"])
            if "modifiers" not in field:
                error(
                    f"Line:{field['line_num']}:{field['col_num']}: Could not find field modifiers"
                )
            field_modifiers = self.create_modifiers_list(field["modifiers"])

            var_object = {
                "super": False,
                "type": f"{field_type}",
                "id": field_name,
                "formal": False,
                "var_type": "field",
                "id_num": field_id,
                "modifiers": field["modifiers"],
                "line_num": field["line_num"],
                "col_num": field["col_num"],
            }
            self.add_to_scope(scope, scope_array, field_name, var_object)

            output += f"FIELD {field_id}, {field_name}, {self.class_name}, {field_modifiers}, {field_type}\n"
        return output

    def create_constructor_record(self, scope, scope_array):
        output = "Constructors:\n"
        for constructor_id in self.constructors.keys():
            local_scope = scope.copy()
            local_scope_array = scope_array.copy()
            constructor = self.constructors[constructor_id]

            if "modifiers" not in constructor:
                error(
                    f"Line:{constructor['line_num']}:{constructor['col_num']}: Could not find constructor modifiers"
                )
            constructor_modifiers = self.create_modifiers_list_PRIVATE_PUBLIC(
                constructor["modifiers"]
            )

            output += f"CONSTRUCTOR: {constructor_id}, {constructor_modifiers}\n"
            output += "Constructor Parameters:\n"

            local_scope = self.add_to_scope(
                scope,
                scope_array,
                constructor_id,
                {
                    "super": False,
                    "type": "constructor",
                    "id": self.class_name,
                    "id_num": constructor_id,
                    "modifiers": constructor["modifiers"],
                    "children": [],
                    "line_num": constructor["line_num"],
                    "col_num": constructor["col_num"],
                },
            )
            local_scope = self.traverse_scope_layer(
                local_scope, [constructor_id, "children"]
            )
            local_scope_array.append(constructor_id)
            local_scope_array.append("children")

            output += "Variable Table:\n"
            for variable_id in constructor["formals"].keys():
                variable = constructor["formals"][variable_id]
                self.add_to_scope(
                    local_scope,
                    local_scope_array,
                    variable["id"],
                    {
                        "super": False,
                        "type": f"{self.create_type_record(variable['type'])}",
                        "id_num": variable_id,
                        "id": variable["id"],
                        "formal": True,
                        "var_type": "local",
                        "line_num": variable["line_num"],
                        "col_num": variable["col_num"],
                    },
                )
                output += self.create_variable_record(variable_id, variable)

            block = self.create_block_record(
                constructor["body"], local_scope, local_scope_array
            )

            output += "Constructor Body:\n"
            output += block
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

            local_scope = self.add_to_scope(
                local_scope,
                local_scope_array,
                method_name,
                {
                    "super": False,
                    "type": "method",
                    "id": method_id,
                    "id_num": method_id,
                    "modifiers": method["modifiers"],
                    "return_type": method["type"],
                    "children": [],
                    "line_num": method["line_num"],
                    "col_num": method["col_num"],
                },
            )
            local_scope = self.traverse_scope_layer(
                local_scope, [method_name, "children"]
            )
            local_scope_array.append(method_name)
            local_scope_array.append("children")

            for variable_id in method["formals"].keys():
                variable = method["formals"][variable_id]
                self.add_to_scope(
                    local_scope,
                    local_scope_array,
                    variable["id"],
                    {
                        "super": False,
                        "type": f"{self.create_type_record(variable['type'])}",
                        "id_num": variable_id,
                        "id": variable["id"],
                        "var_type": "local",
                        "formal": True,
                        "line_num": variable["line_num"],
                        "col_num": variable["col_num"],
                    },
                )
                output += self.create_variable_record(variable_id, variable)

            block = self.create_block_record(
                method["body"], local_scope, local_scope_array
            )

            output += "Variable Table:\n"
            for variable in local_scope:
                for var_id in variable.keys():
                    if variable[var_id]["formal"]:
                        continue
                    output += self.create_variable_record(
                        variable[var_id]["id_num"], variable[var_id]
                    )

            output += "Method Body:\n"
            output += block
        return output

    def create_block_record(self, ast_block, scope, scope_array):
        output = "Block(["
        statements = "\n"
        for statement in ast_block:
            expr = "Expr( "
            stmt = self.create_statement_record(statement, scope, scope_array)
            expr += stmt
            expr += ")\n, "
            if stmt == "":
                expr = ""
            statements += expr
        output += statements
        if output[-3:] == "\n, ":
            output = output[:-2]
        output += "])\n"
        if ast_block == []:
            output = "Skip()"
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
            error(
                f"Line:{ast_type['line_num']}:{ast_type['col_num']}: Invalid type {ast_type}"
            )
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

    def create_statement_record(self, ast_statement, scope, scope_array):
        output = ""
        if ast_statement == None:
            return output
        if "set_equal" in ast_statement:
            output += self.create_assignment_record(ast_statement, scope_array)
        elif "auto" in ast_statement:
            output += self.evaluate_auto(ast_statement, scope, scope_array)
        elif "var_decl" in ast_statement:
            output += self.create_variable_declaration_record(
                ast_statement, scope, scope_array
            )
        elif "return" in ast_statement:
            output += self.evaluate_return(ast_statement, scope, scope_array)
        elif "if" in ast_statement:
            output += self.evaluate_if_block(ast_statement, scope, scope_array)
        elif "while" in ast_statement:
            output += self.evaluate_while_block(ast_statement, scope, scope_array)
        elif "for" in ast_statement:
            output += self.evaluate_for_block(ast_statement, scope, scope_array)
        elif "break" in ast_statement:
            output += "Break"
        elif "continue" in ast_statement:
            output += "Continue"
        elif "method_invocation" in ast_statement:
            output += self.evaluate_method_invo(
                ast_statement["method_invocation"], scope, scope_array
            )
        elif "expression" in ast_statement:
            output += self.create_expression_record(ast_statement, scope, scope_array)
        else:
            error(
                f"Line:{ast_statement['line_num']}:{ast_statement['col_num']}: Invalid statement: {ast_statement}"
            )
        return output

    def create_variable_declaration_record(
        self, ast_variable_declaration, scope, scope_array
    ):
        output = ""
        if "var_decl" not in ast_variable_declaration:
            error(
                f"Line:{ast_variable_declaration['line_num']}:{ast_variable_declaration['col_num']}: Could not find variable declaration"
            )
        variable_declaration = ast_variable_declaration["var_decl"]
        for var in variable_declaration.keys():
            if "id" not in variable_declaration[var]:
                error(
                    f"Line:{ast_variable_declaration['line_num']}:{ast_variable_declaration['col_num']}: Could not find variable id"
                )
            if "type" not in variable_declaration[var]:
                error(
                    f"Line:{ast_variable_declaration['line_num']}:{ast_variable_declaration['col_num']}: Could not find variable type"
                )

            var_id = variable_declaration[var]["id"]
            var_type = variable_declaration[var]["type"]
            self.add_to_scope(
                scope,
                scope_array,
                var_id,
                {
                    "super": False,
                    "type": f"{self.create_type_record(var_type)}",
                    "id_num": var,
                    "id": var_id,
                    "var_type": "local",
                    "formal": False,
                    "line_num": variable_declaration[var]["line_num"],
                    "col_num": variable_declaration[var]["col_num"],
                },
            )
            output += self.create_variable_record(var, variable_declaration[var])

        return ""

    def create_assignment_record(self, ast_assignment, scope_array):
        if "set_equal" not in ast_assignment:
            error(
                f"Line:{ast_variable_declaration['line_num']}:{ast_assignment['col_num']}: Could not find assignment"
            )
        output = ""
        assignment = ast_assignment["set_equal"]
        if "assign" not in assignment:
            error(
                f"Line:{ast_variable_declaration['line_num']}:{ast_assignment['col_num']}: Could not find assignee "
            )

        operand = assignment["assign"]
        var_id_num, var_type = self.get_var_from_scope(
            operand["assignee"]["field_access"]["id"], scope_array
        )

        expr_type = "Assign"
        var_scope_type = "Variable"
        if "field_" in var_type:
            var_scope_type = "Field-access"

        assignee = f"{var_id_num}"

        assigned_value = ""
        if "assigned_value" not in operand:
            error(
                f"ine:{operand['assignee']['line_num']}:{operand['assignee']['col_num']}: Could not find assigned value"
            )

        if "expression" in operand["assigned_value"]:
            assigned_value = self.create_expression_record(
                operand["assigned_value"], scope, scope_array
            )
        else:
            error(
                f"Line:{operand['assignee']['line_num']}:{operand['assignee']['col_num']}: Could not find assigned value type"
            )

        expression = f"{var_scope_type}({assignee}), {assigned_value} "
        if expr_type != "":
            output += f"{expr_type}({expression})"
        else:
            output += expression

        return output

    def create_expression_record(self, ast_expression, scope, scope_array):
        if "expression" not in ast_expression:
            error(
                f"line:{ast_expression['line_num']}:{ast_expression['col_num']}: Could not find expression in {ast_expression}"
            )
        expression = ast_expression["expression"]
        output = ""
        if "field_access" in expression:
            primary = self.evaluate_primary(
                expression["field_access"], scope, scope_array
            )
            output += (
                f"Field-access({primary})"
                if expression["field_access"]["primary"] != ""
                else f"Variable({self.get_var_from_scope(primary, scope_array)[0]})"
            )
        elif "literal" in expression:
            output += self.evaluate_literal(expression["literal"])
        elif "method_invocation" in expression:
            output += self.evaluate_method_invo(
                expression["method_invocation"], scope, scope_array
            )
        elif "binary_expression" in expression:
            output += self.evaluate_binary_expression(expression, scope, scope_array)
        elif "unary_expression" in expression:
            output += self.evaluate_unary_expression(expression, scope, scope_array)
        elif "literal" in expression:
            output += self.evaluate_literal(expression["literal"])
        elif "new" in expression:
            output += self.evaluate_new_object(expression["new"], scope, scope_array)
        elif "auto" in expression:
            output += self.evaluate_auto(expression, scope, scope_array)
        elif "set_equal" in expression:
            output += self.create_assignment_record(expression, scope_array)
        elif "this" == expression:
            output += "this"
        elif "expression" in expression:
            output += self.create_expression_record(expression, scope, scope_array)
        else:
            error(
                f"Line:{expression['line_num']}:{expression['col_num']}: Invalid expression statement"
            )
        return output

    def evaluate_auto(self, ast_auto, scope, scope_array):
        if "auto" not in ast_auto:
            error(
                f"Line:{ast_auto['line_num']}:{ast_auto['col_num']}: Could not find auto"
            )
        output = ""
        assigned_value = ""
        auto = ast_auto["auto"]
        if "operand" not in auto:
            error(f"{auto['line_num']}:{auto['col_num']}: Could not find operand")
        variable_name = auto["operand"]["field_access"]["id"]
        var_id = self.get_var_from_scope(variable_name, scope_array)[0]
        if "postfix" in auto:
            assigned_value = f"Variable({var_id}), {auto['postfix']}, post"
        elif "prefix" in auto:
            assigned_value = f"Variable({var_id}), {auto['prefix']}, pre"
        output += f"Auto({assigned_value})"
        return output

    def evaluate_if_block(self, ast_if, scope, scope_array):
        output = ""
        if "if" not in ast_if:
            error(f"line:{ast_if['line_num']}:{ast_if['col_num']}: Could not find if")
        if_block = ast_if["if"]
        if "condition" not in if_block:
            error(
                f"Line:{if_block['line_num']}:{if_block['col_num']}: Could not find condition"
            )
        if "if_block" not in if_block:
            error(
                f"line:{if_block['line_num']}:{if_block['col_num']}: Could not find block"
            )
        condition = self.create_expression_record(
            if_block["condition"], scope, scope_array
        )
        block = self.create_block_record(if_block["if_block"], scope, scope_array)
        output += f"If({condition}, {block}"
        if "else_block" in if_block:
            output += ", "
            output += self.create_block_record(
                if_block["else_block"], scope, scope_array
            )
        output += ")"
        return output

    def evaluate_while_block(self, ast_while, scope, scope_array):
        output = ""
        if "while" not in ast_while:
            error(
                f"Line:{ast_while['line_num']}:{ast_while['col_num']}: Could not find while"
            )
        while_block = ast_while["while"]
        if "condition" not in while_block:
            error(
                f"Line:{while_block['line_num']}:{while_block['col_num']}: Could not find condition"
            )
        if "while_block" not in while_block:
            error(
                f"Line:{while_block['line_num']}:{while_block['col_num']}: Could not find block"
            )
        condition = self.create_expression_record(
            while_block["condition"], scope, scope_array
        )
        block = self.create_block_record(while_block["while_block"], scope, scope_array)
        if block[-1] == "\n":
            block = block[:-1]
        output += f"While({condition}, {block})"
        return output

    def evaluate_for_block(self, ast_for, scope, scope_array):
        output = ""
        if "for" not in ast_for:
            error(
                f"Line:{ast_for['line_num']}:{ast_for['col_num']}: Could not find for"
            )
        for_block = ast_for["for"]
        if "condition" not in for_block:
            error(
                f"Line:{for_block['line_num']}:{for_block['col_num']}: Could not find condition"
            )
        if "for_block" not in for_block:
            error(
                f"Line:{for_block['line_num']}:{for_block['col_num']}: Could not find block"
            )
        if "init" not in for_block:
            error(
                f"Line:{for_block['line_num']}:{for_block['col_num']}: Could not find init"
            )
        if "update" not in for_block:
            error(
                f"Line:{for_block['line_num']}:{for_block['col_num']}: Could not find update"
            )
        init = (
            self.create_expression_record(for_block["init"], scope, scope_array)
            if for_block["init"] != None
            else "Skip()"
        )
        update = (
            self.create_expression_record(for_block["update"], scope, scope_array)
            if for_block["update"] != None
            else "Skip()"
        )
        condition = (
            self.create_expression_record(for_block["condition"], scope, scope_array)
            if for_block["condition"] != None
            else "Skip()"
        )
        block = self.create_block_record(for_block["for_block"], scope, scope_array)
        output += f"For({init}, {condition}, {update}, {block})"
        return output

    def evaluate_unary_expression(self, ast_unary, scope, scope_array):
        output = ""
        if "unary_expression" not in ast_unary:
            error(
                f"Line:{ast_unary['line_num']}:{ast_unary['col_num']}: Could not find unary expression"
            )
        unary_expression = ast_unary["unary_expression"]
        if "operator" not in unary_expression:
            error(
                f"Line:{unary_expression['line_num']}:{unary_expression['col_num']}: Could not find operator"
            )
        expression = self.create_expression_record(
            unary_expression["operand"], scope, scope_array
        )
        operator_to_string = {"-": "uminus", "!": "neg"}
        if unary_expression["operator"] == "+":
            return expression

        operator = ""
        if unary_expression["operator"] in operator_to_string:
            operator = operator_to_string[unary_expression["operator"]]
        output += f"Unary({expression}, {operator})"
        return output

    def evaluate_binary_expression(self, ast_binary, scope, scope_array):
        output = ""
        if "binary_expression" not in ast_binary:
            error(
                f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find binary expression"
            )

        binary_expression = ast_binary["binary_expression"]
        if "left" not in binary_expression:
            error(
                f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find left operand"
            )
        if "right" not in binary_expression:
            error(
                f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find right operand"
            )
        if "operator" not in binary_expression:
            error(
                f"Line{binary_expression['line_num']}:{binary_expression['col_num']}: Could not find operator"
            )
        left_expression = self.create_expression_record(
            binary_expression["left"], scope, scope_array
        )
        right_expression = self.create_expression_record(
            binary_expression["right"], scope, scope_array
        )
        operator = binary_expression["operator"]

        operator_to_string = {
            "+": "add",
            "-": "sub",
            "*": "mul",
            "/": "div",
            "%": "mod",
            "&&": "and",
            "||": "or",
            "==": "eq",
            "!=": "neq",
            "<": "lt",
            ">": "gt",
            "<=": "leq",
            ">=": "geq",
        }

        if operator not in operator_to_string:
            error(f"Line{operator['line_num']}:{operator['col_num']}: Invalid operator")

        operator = operator_to_string[operator]
        output += f"Binary({operator}, {left_expression}, {right_expression})"
        return output

    def evaluate_return(self, ast_return, scope, scope_array):
        output = ""
        if "return" not in ast_return:
            error(
                f"{ast_return['line_num']}:{ast_return['col_num']}: Could not find return"
            )
        statement_eval = self.create_expression_record(
            ast_return["return"], scope, scope_array
        )
        output += f"Return({statement_eval})"
        return output

    def evaluate_method_invo(self, ast_method_invo, scope, scope_array):
        output = ""
        if "field_access" not in ast_method_invo:
            error(
                f"Line:{ast_method_invo['line_num']}:{ast_method_invo['col_num']}: Could not find method field_access"
            )
        if "arguments" not in ast_method_invo:
            error(
                f"Line:{ast_method_invo['line_num']}:{ast_method_invo['col_num']}: Could not find method arguments"
            )
        method = ast_method_invo["field_access"]
        if "id" not in method:
            error(
                f"Line:{method['line_num']}:{method['col_num']}: Could not find method id "
            )
        if "primary" not in method:
            error(
                f"Line:{method['line_num']}:{method['col_num']}: Could not find method primary"
            )

        arguments = ast_method_invo["arguments"]
        arg_str = []
        for arg in arguments:
            arg_str.append(self.create_expression_record(arg, scope, scope_array))
        arg_str = ", ".join(arg_str)
        output += f"Method-call({self.evaluate_primary(method,scope,scope_array)}, [{arg_str}])"
        return output

    def evaluate_literal(self, ast_literal):
        output = ""
        if "type" not in ast_literal:
            error(
                f"Line:{ast_literal['line_num']}:{ast_literal['col_num']}: Could not find literal type"
            )
        if "value" not in ast_literal:
            error(
                f"Line:{ast_literal['line_num']}:{ast_literal['col_num']}: Could not find literal value"
            )
        if ast_literal["type"] == "boolean" or ast_literal["type"] == "Null":
            output += f"Constant({ast_literal['value']})"
        else:
            output += f"{ast_literal['type']}-Constant({ast_literal['value']})"
        return output

    def evaluate_new_object(self, ast_new_object, scope, scope_array):
        output = ""
        arguments = ast_new_object["arguments"]
        arg_str = []
        for arg in arguments:
            arg_str.append(self.create_expression_record(arg, scope, scope_array))
        arg_str = ", ".join(arg_str)

        output += f"New-object({ast_new_object['type']}, [{arg_str}])"
        return output

    def evaluate_primary(self, ast_primary, local_scope, scope_array):
        output = ast_primary["id"]
        if ast_primary["primary"] != "":
            primary = ast_primary["primary"]
            global scope

            if "field_access" in primary:
                primary = self.evaluate_primary(
                    primary["field_access"], scope, scope_array
                )
            primary_array = primary.split(", ")
            save_primary = primary_array.copy()
            primary = primary_array.pop(0)
            cont = True
            current_scope = scope["global"]
            while cont:
                if len(primary_array) == 0:
                    cont = False
                    continue
                searching_for = primary_array.pop(0)
                desired_super = False
                if primary.lower() == "this":
                    primary = self.class_name
                    current_scope = current_scope[primary]
                elif primary.lower() == "super":
                    desired_super = True
                    primary = self.class_name
                    current_scope = current_scope[primary]
                else:
                    if len(primary_array) > 1:
                        if "children" in current_scope:
                            current_scope = current_scope["children"]
                        else:
                            if isinstance(current_scope, dict):
                                if searching_for in current_scope:
                                    current_scope = current_scope[searching_for]
                                else:
                                    error(
                                        f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope"
                                    )
                            elif isinstance(current_scope, list):
                                found = False
                                for child in current_scope:
                                    if searching_for in child:
                                        current_scope = child[searching_for]
                                        found = True
                                if not found:
                                    error(
                                        f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope"
                                    )
                primary = searching_for

            if primary == "this":
                found = 0
                for child in scope["global"][self.class_name]["children"]:
                    if ast_primary["id"] in child:
                        found = 1
                if found == 0:
                    error(
                        f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope"
                    )

            elif primary == "super":
                found = 0

                for child in scope["global"][self.class_name]["children"]:
                    if ast_primary["id"] in child:
                        if child[ast_primary["id"]]["super"]:
                            found = 1

                if found == 0:
                    error(
                        f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope"
                    )

            elif primary == "":
                if isinstance(local_scope, list):
                    for child in local_scope:
                        if ast_primary["id"] in scope:
                            if not child[ast_primary["id"]]["super"]:
                                found = 1
                elif isinstance(local, dict):
                    if ast_primary["id"] in scope:
                        if not local_scope[ast_primary["id"]]["super"]:
                            found = 1
                if found == 0:
                    error(
                        f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope"
                    )
            else:
                if primary not in scope["global"]:
                    var = self.get_var_from_scope(primary, scope_array)
                    if var == None:
                        error(
                            f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find primary in scope"
                        )
                    var_type = var[1]
                    if "user(" in var_type:
                        var_type = var_type.replace("user(", "")[:-1]
                    elif "method" in var_type:
                        pass

                    if var_type not in scope["global"]:
                        error(
                            f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find primary in scope"
                        )
                    found = 0
                    for child in scope["global"][var_type]["children"]:
                        if ast_primary["id"] in child:
                            warn(child[ast_primary["id"]])
                            found = 1
                    if found == 0:
                        error(
                            f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope"
                        )
                else:
                    found = 0
                    for child in scope["global"][primary]["children"]:
                        if ast_primary["id"] in child:
                            found = 1
                    if found == 0:
                        error(
                            f"Line:{ast_primary['line_num']}:{ast_primary['col_num']}: Could not find identifier in scope"
                        )

            if "this" == primary or "super" == primary:
                primary = primary.title()
            output = ", ".join(save_primary)
            output += ", "
            output += ast_primary["id"]
        return output

    def traverse_scope_layer(self, scope, scope_layers):
        new_scope = scope.copy()
        for scope_layer in scope_layers:
            if isinstance(new_scope, list):
                found = False
                for scope_item in new_scope:
                    if scope_layer in scope_item:
                        new_scope = scope_item[scope_layer]
                        found = True
                if not found:
                    error(f"Could not find scope layer at {scope_layer}")
            elif isinstance(new_scope, dict):
                if scope_layer in new_scope:
                    new_scope = new_scope[scope_layer]
                else:
                    error(f"Could not find scope layer: {scope_layer} in {new_scope}")
            else:
                error(f"Invalid scope layer traversal at {new_scope}, {scope_layer}")
        return new_scope

    def add_to_scope(self, local_scope, scope_array, variable_id, variable):
        self.check_current_scope(local_scope, variable_id, {variable_id: variable})

        global scope
        legal_types = ["class", "method", "constructor"]

        if scope_array == []:
            scope_array = ["global"]
        test_scope = scope
        for scope_layer in scope_array:
            if isinstance(test_scope, list):
                for scope_item in test_scope:
                    if variable_id in scope_item:
                        if (
                            variable["type"] == scope_item[variable_id]["type"]
                            and scope_item[variable_id]["var_type"]
                            == variable["var_type"]
                            and scope_item[variable_id]["super"]
                        ):
                            error(
                                f"Line:{variable['line_num']}:{variable['col_num']}: Variable already defined: {variable_id}"
                            )
                        if (
                            scope_item[variable_id]["type"] not in legal_types
                            and variable["type"] not in legal_types
                        ):
                            if (
                                scope_item[variable_id]["var_type"]
                                == variable["var_type"]
                            ):
                                error(
                                    f"Line:{variable['line_num']}:{variable['col_num']}: Variable already defined: {variable_id}"
                                )
            else:
                if variable_id in test_scope:
                    if (
                        variable["type"] == test_scope[variable_id]["type"]
                        and scope_item[variable_id]["var_type"] == variable["var_type"]
                    ):
                        error(
                            f"Line{variable['line_num']}:{variable['col_num']}: Variable already defined: {variable_id}"
                        )
                    if (
                        test_scope[variable_id]["type"] not in legal_types
                        and variable["type"] not in legal_types
                    ):
                        if scope_item[variable_id]["var_type"] == variable["var_type"]:
                            error(
                                f"Line:{variable['line_num']}:{variable['col_num']}: Variable already defined: {variable_id}"
                            )
            test_scope = self.traverse_scope_layer(test_scope, [scope_layer])

        if isinstance(local_scope, list):
            local_scope.append({variable_id: variable})
        else:
            local_scope[variable_id] = variable
        return local_scope

    def get_var_from_scope(self, variable_name, scope_array, class_var=0):
        global scope
        if scope_array == []:
            scope_array = ["global"]

        test_scope = scope
        illegal_types = ["class", "method", "constructor"]
        for scope_layer in scope_array:
            test_scope = self.traverse_scope_layer(test_scope, [scope_layer])
            if isinstance(test_scope, list):
                for scope_item in test_scope:
                    if variable_name in scope_item:
                        if scope_item[variable_name]["type"] in illegal_types:
                            continue
                        return [
                            scope_item[variable_name]["id_num"],
                            scope_item[variable_name]["type"],
                        ]
            else:
                if variable_name in test_scope:
                    if test_scope[variable_name]["type"] in illegal_types:
                        continue
                    return [
                        test_scope[variable_name]["id_num"],
                        test_scope[variable_name]["type"],
                    ]
        error(f"Variable not found: {variable_name}")

    def check_current_scope(self, scope, id_, item):
        for scope_item in scope:
            if id_ in scope_item:
                if compare_var(scope_item[id_], item[id_]):
                    error(
                        f"Line:{item[id_]['line_num']}:{item[id_]['col_num']} Variable already defined: {id_}"
                    )
        return scope


def readJSON(filename):
    with open(filename, "r") as infile:
        data = json.load(infile)
    return data


def writeAST(ast_blocks):
    output = "-----------------------------------------------\n"
    for ast in ast_blocks:
        if ast == None:
            continue
        output += ast.print_ast()
        output += "-----------------------------------------------\n"
    return output


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
        if "field" in item:
            for id_name in item["field"]["ids"]:
                fields[field_count] = item["field"]
                fields[field_count]["id"] = id_name
                del fields[field_count]["ids"]
                field_count += 1
        elif "method" in item:
            methods[method_count] = item["method"]
            method_count += 1
        elif "constructor" in item:
            constructors[class_count] = item["constructor"]
            class_count += 1
        else:
            error(
                f"Could not find field, method, or constructor at line:{['line_num']}:{['col_num']}"
            )
    ast["body"] = {"fields": fields, "methods": methods, "constructors": constructors}
    return AST(ast, fields, methods, constructors)


def extract_variables_from_formals(key, ast):
    global var_count

    if key not in ast:
        raise Exception(f"Could not find {key}")

    if "formals" not in ast[key]:
        raise Exception(f"Could not find formals in {key}")

    params = {}

    for item in ast[key]["formals"]:
        if "parameter" not in item:
            raise Exception("Could not find parameter in formals item")
        item["parameter"]["var_type"] = "local"
        params[var_count] = item["parameter"]
        var_count += 1  #

    ast[key]["formals"] = params
    return ast


def extract_variables_from_field(ast):
    if "field" not in ast:
        raise Exception("Could not find field")
    if "variables" not in ast["field"]:
        raise Exception("Could not find variables")
    if "type" not in ast["field"]["variables"]:
        raise Exception("Could not find type")
    if "ids" not in ast["field"]["variables"]:
        raise Exception("Could not find ids")
    ast["field"]["type"] = ast["field"]["variables"]["type"]
    ast["field"]["ids"] = ast["field"]["variables"]["ids"]
    ast["field"]["col_num"] = ast["field"]["variables"]["col_num"]
    ast["field"]["line_num"] = ast["field"]["variables"]["line_num"]
    del ast["field"]["variables"]
    return ast


def compare_var(obj1, obj2):
    if obj1 == obj2:
        return True

    if not (isinstance(obj1, dict) and isinstance(obj2, dict)):
        return False

    for key in ("type", "id", "var_type"):
        if key not in obj1 or key not in obj2 or obj1[key] != obj2[key]:
            return False

    return True
