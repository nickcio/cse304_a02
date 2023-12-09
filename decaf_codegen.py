# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

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
  pass

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


def generatebinexprtype(ast_binary, Lnum, data, register_left, register_right, registers: list(), operator_to_string):
  pass

def generatebitflip(register, registers: list(), Lnum):
  pass

def generateforfooter(count):
  pass

def generateiffooter(count):
  pass

def generatemove(reg1,reg2):
  pass

def generatejump(label):
  pass

def generatereturn(register):
  pass

def generateauto(ast_auto, register, _type, registers: list()):
  pass

def generateifhead(ast_if, register, count):
  pass

def generateelsehead(ast_if, count):
  pass

def generatewhilehead(ast_while, count):
  pass

def generatewhilecond(register, count):
  pass

def generatewhilefoot(count):
  pass