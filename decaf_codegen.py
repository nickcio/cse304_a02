# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

def error(string):
    RED = "\033[91m"
    CLEAR_COLOR = "\033[0m"
    print(f"{RED}ERROR:{CLEAR_COLOR} {string}", file=sys.stderr)
    exit(1)

def generateprog(astprog):
    return ""
  
def generatelabel(label):
    return f'\n{label}:\n'
  
def generatecommlabel(label,comm):
    return f'\n# {comm}\n{label}:\n'
  
def generatecomm(comm):
    return f'# {comm}\n'
  
def generatemethod(method, methodid, data: dict()):
    out = f'\n# method {methodid}\n'
    methodname = methodid
    out += generatelabel(f"{data['class_name']}_{methodname}")
    return out


def generatefield(ast_field, field_size, data: dict(), registers: list()):
    out = f"\n# field {ast_field['field_id']}: {ast_field['name']} - {ast_field['line_num']}:{ast_field['col_num']}\n"
    reg = registers.pop(0)
    out+=f'move_immed_i {reg}, {str(field_size)}\n'
    out+= f'halloc sap, {reg}\n'
    data[f'FIELD_{ast_field["field_id"]}'] = reg
    return out, registers, data

def generateblock(ast_block):
    return ""
  
def generatestmt(ast_statement):
    return ""

def generateexpr(ast_expression, registers: list()):
    return "", registers.pop(0)

def generategetfieldval(register, registers: list()):
    reg = registers.pop(0)
    out = f'hload {reg}, sap, {register}\n'
    return out, reg

def generatemethodcall(method_label):
    return f'call {method_label}\n'

def generateliteral(value, registers: list(), isfloat=False):
    reg = registers.pop(0)
    out = ""
    if isfloat: out = f'move_immed_f {reg}, {value}\n'
    else: out = f'move_immed_i {reg}, {value}\n'
    return out, reg

def generateforhead(ast_for, count):
    return f"\n# for expression {ast_for['line_num']}:{ast_for['col_num']}\nfor_{count}\n"

def generateforcond(ast_for, count, register1):
    return f'bz {register1}, endfor_{count}\n'

def generatehstore(register, field_register):
    return f'hstore sap, {field_register}, {register}\n'

def generateinit(important_registers: list(), constructor_id, registers: list(), size):
    out = generatecomm(f'create new obj w/ constructor C_{constructor_id}\n')
    sizereg = registers.pop(0)
    out+=f'move_immediate_i {sizereg}, {size}\n'
    out+=f'halloc sap, {sizereg}\n'
    for reg in important_registers: out+=f'save {reg}\n'
    out+=f'save {sizereg}\n'
    out+=f'call C_{constructor_id}\n'
    for reg in important_registers: out+=f'restore {reg}\n'
    out+=f'restore {sizereg}\n'
    return out
       
def generateneg(register, registers: list()):
    out = ""
    reg = registers.pop(0)
    out += f"move_immediate_i {reg}, -1\n"
    out += f'imul {register}, {register}, {reg}\n'
    out += f'# free {reg}'
    return out

def getvreg(var_id, asm_data):
    if var_id in asm_data: return asm_data[var_id]
    else: return "None"

def generatebinexpr(ast_binary, Lnum, data, register_left, register_right, registers: list(), _type="int"):
  
    int_ops = {
        "+": "iadd",
        "-": "isub",
        "*": "imul",
        "/": "idiv",
        "%": "imod",
        "&&": "and",
        "||": "or",
        "==": "eq",
        "!=": "neq",
        "<": "ilt",
        ">": "igt",
        "<=": "ileq",
        ">=": "igeq"
    }
  
    float_ops = {
        "+": "fadd",
        "-": "fsub",
        "*": "fmul",
        "/": "fdiv",
        "%": "fmod",
        "&&": "and",
        "||": "or",
        "==": "eq",
        "!=": "neq",
        "<": "flt",
        ">": "fgt",
        "<=": "fleq",
        ">=": "fgeq"
    }
  
    if _type == "float":
        return generatebinexprtype(ast_binary, Lnum, data, register_left, register_right, registers, float_ops)
    else:
        return generatebinexprtype(ast_binary, Lnum, data, register_left, register_right, registers, int_ops)

def generatebinexprtype(ast_binary, Lnum, data, register_left, register_right, registers: list(), operatorstr):
    if "binary_expression" not in ast_binary:
        error(f'ERROR: Could not find binary expression')
    binexpr = ast_binary["binary_expression"]
    out = ""
    if "left" not in binexpr: error(f"Line{binexpr['line_num']}:{binexpr['col_num']}: Could not find left operand")
    if "right" not in binexpr: error(f"Line{binexpr['line_num']}:{binexpr['col_num']}: Could not find right operand")
    if "operator" not in binexpr: error(f"Line{binexpr['line_num']}:{binexpr['col_num']}: Could not find operator")
    operator = binexpr['operator']
    if operator not in operatorstr: error(f"Line{operator['line_num']}:{operator['col_num']}: Invalid operator")
    operator = operatorstr[operator]
    regout = registers.pop(0)
    if operator == "eq":
        out += f"beq {register_left}, {register_right}, L_{Lnum}_TRUE\n"
        out += f"move_immed_i {regout}, 0\n"
        out += f"jmp L_{Lnum}_E\n"
        out += f"L_{Lnum}_T:\n"
        out += f"move_immed_i {regout}, 1\n"
        out += f"L_{Lnum}_E:\n"  
    elif operator == "neq":
        out += f"beq {register_left}, {register_right}, L_{Lnum}_TRUE\n"
        out += f"move_immed_i {regout}, 1\n"
        out += f"jmp L_{Lnum}_E\n"
        out += f"L_{Lnum}_T:\n"
        out += f"move_immed_i {regout}, 0\n"
        out += f"L_{Lnum}_E:\n"
    out += f'{operator} {regout}, {register_left}, {register_right}\n' 
    return out, registers, regout

def generatebitflip(register, registers: list(), Lnum):
    reg = registers.pop(0)
    out = f"move_immed_i {reg}, 1\n"
    out += f"beq {reg}, {register}, L_{Lnum}_TRUE\n"
    out += f"move_immed_i {register}, 1\n"
    out += f"jmp L_{Lnum}_E\n"
    out += f"L_{Lnum}_T:\n"
    out += f"move_immed_i {register}, 0\n"
    out += f"L_{Lnum}_E:\n"
    return out

def generateforfooter(count):
    return generatelabel(f'endfor_{count}')

def generateiffooter(count):
    return generatelabel(f'endif_{count}')

def generatemove(reg1,reg2):
    return f'move {reg1} {reg2}\n'

def generatejump(label):
    return f'jmp {label}\n'

def generatereturn(register):
    return f'move a0, {register}\nret\n'

def generateauto(ast_auto, register, _type, registers: list()):
    if "auto" not in ast_auto: error(f"Line{ast_auto['line_num']}:{ast_auto['col_num']}: Could not find auto")
    auto = ast_auto["auto"]

    reg = registers.pop(0)
    out = f'move_immediate_i {reg},'
    value = ""
    if "postfix" in auto: value = auto['postfix']      
    elif "prefix" in auto: value = auto['prefix']
    else: error(f"Line{auto['line_num']}:{auto['col_num']}: Could not find prefix or postfix")
    if "inc" in value: out += "1\n"
    elif "dec" in value: out += "-1\n"
    else: error(f"Line{auto['line_num']}:{auto['col_num']}: Invalid postfix or prefix")

    if _type == "float":
        out += f'ftoi {reg}, {reg}\n'
        out += f'fadd {register}, {register}, {reg}\n'
    else:
        out += f'iadd {register}, {register}, {reg}\n'
    return out, register

def generateifhead(ast_if, register, count):
    return f'bnz {register}, else_{count}\n'

def generateelsehead(ast_if, count):
    return f'jmp endif_{count}\nelse_{count}:\n'

def generatewhilehead(ast_while, count):
    return f'while_{count}:'

def generatewhilecond(register, count):
    return f'bz {register}, endwhile_{count}\n'

def generatewhilefoot(count):
    return f'jmp while_{count}\nendwhile{count}:\n'