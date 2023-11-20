# Nicholas Ciotoli 113325368 nciotoli
# Adam Lipson 114339915 alipson

from decaf_ast import valid_types

def is_subtype(scope,type1,type2):
    elems = {"Integer":"int","Float":"float","String":"string","Boolean":"boolean"}
    if type1 in elems: type1=elems[type1]
    elif type2 in elems: type2=elems[type2]
    elif type1==type2: return True
    elif type1.lower()=="null" and "user(" in type2: return True
    elif type1=="int" and type2=="float": return True
    elif "user(" in type1 and "user(" in type2: return is_subclass(scope,type1,type2)
    elif "class-literal(" in type1 and "class-literal(" in type2: return is_subclass(scope,type1,type2)
    return False

def is_subclass(scope,type1,type2):
    if type1 == type2: return True
    elif type1.lower()=="null" and "user(" in type2: return True
    elif ("user(" in type1 and "user(" in type2) or ("class-literal(" in type1 and "class-literal(" in type2):
        if "user(" in type1:
            type1name = type1[6:-1]
            type2name = type2[6:-1]
        else:
            type1name = type1[15:-1]
            type2name = type2[15:-1]
        if type1name in scope["global"]:
            while scope["global"][type1name]["superclass_name"] != "" and type2name != type2name:
                type1 = scope["global"][type1]["superclass_name"]
                if type1 == type2: return True
    return False
          