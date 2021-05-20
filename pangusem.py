#pangusem
#symbol table
from xnames import *
from ptree import *
from pangusymtab import *
from pangulex import *

symtab = SymbolTab()
is_attri = False

scope_stack = []
scope_stack1 = []

current_type = ''

def symtab_check(id,scope):
    global symtab
    global scope_stack
    for s in symtab.table:
        if s.name == id and (s.scope in scope_stack): ##need to consider more later!!
            return True
    return False

# x_arg_list -> [x_const] x_atype x_id [x_arg_list_tail]
# x_atype -> x_bool [x_dim] [x_at]
#         -> x_char [x_dim] [x_at]
#         -> x_string [x_dim] [x_at]
#         -> x_int [x_dim] [x_at]
#         -> x_float [x_dim] [x_at]
#         -> x_id [x_dim] [x_at]
def get_signature1(node):
    if node.nodeid != x_arg_list:
        print('get_signature error 1')
        sys.exit(0)
    if node.children[0].nodeid == x_const:
        n = node.children[1]
        index = 1
    else:
        n = node.children[0]
        index = 0
    if n.nodeid  != x_atype:
        print('get_signature error 2')
        sys.exit(0)
    if n.children[0].nodeid == x_id:
        s = n.children[0].value
    else:
        s = ss(n.children[0])[2:]
    if n.children[1].nodeid == x_dim:
        d = n.children[1].value
    else:
        d = 0
    for i in range(d):
        s += "[]"
    signature = [s]
    if len(node.children) < 3+index:
        return signature
    else:
        return get_signature2(node.children[2+index],signature)

# x_arg_list_tail -> [x_const] x_atype x_id [x_arg_list_tail]
# x_atype -> x_bool [x_dim] [x_at]
#         -> x_char [x_dim] [x_at]
#         -> x_string [x_dim] [x_at]
#         -> x_int [x_dim] [x_at]
#         -> x_float [x_dim] [x_at]
#         -> x_id [x_dim] [x_at]
def get_signature2(node,signature):
    if node.nodeid != x_arg_list_tail:
        print('get_signature error 1')
        sys.exit(0)
    if node.children[0].nodeid == x_const:
        n = node.children[1]
        index = 1
    else:
        n = node.children[0]
        index = 0
    if n.nodeid  != x_atype:
        print('get_signature error 2')
        sys.exit(0)
    if n.children[0].nodeid == x_id:
        s = n.children[0].value
    else:
        s = ss(n.children[0])[2:]
    if n.children[1].nodeid == x_dim:
        d = n.children[1].value
    else:
        d = 0
    for i in range(d):
        s += "[]"
    signature.append(s)
    if len(node.children) < 3+index:
        return signature
    else:
        return get_signature2(node.children[2+index],signature)

def get_atype(n):
    if n.children[0].nodeid == x_id:
        s = n.children[0].value
    else:
        s = ss(n.children[0])[2:]
    if n.children[1].nodeid == x_dim:
        d = n.children[1].value
    else:
        d = 0
    for i in range(d):
        s += "[]"
    return s

def get_type(n):
    s = n.children[0].value
    if len(n.children) > 1:
        d = n.children[1].value
    else:
        d = 0
    for i in range(d):
        s += "[]" 
    return s

def sub_seman(node,parent):
    global symtab
    global scope_stack
    global is_attri
    global current_type

    if node.nodeid == x_compilation_unit:
        scope_stack.append('global')
        return
    
    #endmain condition
    if node.nodeid == x_main_body:
        if node.leaf():
            scope_stack.pop()
            return
    #main
    if node.nodeid == x_main_section:
        scope_stack.append('main')
        return

    #class
    if node.nodeid == x_class_header:
        length = len(node.children)
        classname = node.children[0].value
        a = symtab.is_classname(classname)
        if a:
            print("classname: ",classname," already existed!")
            sys.exit(0)
        symtab.insertSymbol(id=classname,scope=scope_stack[-1],kind="classname")
        if length == 2:
            if node.children[1].nodeid == x_id:
                extends_classname = node.children[1].value
                b = symtab.is_classname(extends_classname)
                if not b:
                    print("classname error : ",extends_classname," not found!")
                    sys.exit(0)
        elif length == 3:
            extends_classname = node.children[1].value
            b = symtab.is_classname(extends_classname)
            if not b:
                print("classname error : ",extends_classname," not found!")
                sys.exit(0)
        #new scope
        scope_stack.append(classname)
        return
    
    #method
    if node.nodeid == x_method_header:
        name = node.children[1].value
        if len(node.children) >= 3:
            if node.children[2].nodeid == x_arg_list:
                signature = get_signature1(node.children[2])
            else:
                signature = []
        else:
            signature = []
        a = symtab.is_classname(name)
        if a: #constr
            b = symtab.is_constr(name,scope_stack[-1],signature)
            if b:
                print("constructor: ",name," existed!")
                sys.exit(0)
            else:
                symtab.insertSymbol(id=name,scope=scope_stack[-1],kind="constr",signature=signature)
        else: # method
            c = symtab.is_method(name,scope_stack[-1],signature)
            if c:
                print("method: ",name," existed!")
                sys.exit(0)
            else:
                symtab.insertSymbol(id=name,scope=scope_stack[-1],kind="methodname",signature=signature)
        #new scope
        new_scope = scope_stack[-1]+'.'+name
        scope_stack.append(new_scope)
        return

    #endmethod condition
    if node.nodeid == x_method_body:
        if node.leaf():
            scope_stack.pop()
            return
    #endclass condition
    if node.nodeid == x_class_body:
        if len(node.children) == 0:
            scope_stack.pop()
            return
    
    #var_list
    if node.nodeid == x_var_list:
        varname = node.children[0].value
        if symtab.is_var(varname,scope_stack[-1]):
            print("error: ",varname," is already defined!")
            sys.exit(0)
        if symtab.is_attribute(varname,scope_stack[-1]):
            print("error: ",varname," is already defined!")
            sys.exit(0)
        if symtab.is_arg(varname,scope_stack[-1]):
            print("error: ",varname," is already defined as arguement in the method!")
            sys.exit(0)
        if symtab.is_methodname(varname,scope_stack[-1]):
            print("error: ",varname," is already defined as method!")
            sys.exit(0)
        if symtab.is_classname(varname):
            print("error: ",varname," is already defined as a class!")
            sys.exit(0)
        if parent.nodeid == x_attr_definition:
            symtab.insertSymbol(id=varname,scope=scope_stack[-1],kind="attribute",type=current_type)
            is_attri = True
        else:
            symtab.insertSymbol(id=varname,scope=scope_stack[-1],kind="var",type=current_type)
            is_attri = False
        return

    #var_list_tail
    if node.nodeid == x_var_list_tail:
        varname = node.children[0].value
        if symtab.is_var(varname,scope_stack[-1]):
            print("error: ",name," is already defined!")
            sys.exit(0)
        if symtab.is_attribute(varname,scope_stack[-1]):
            print("error: ",varname," is already defined!")
            sys.exit(0)
        if symtab.is_arg(varname,scope_stack[-1]):
            print("error: ",varname," is already defined as arguement in the method!")
            sys.exit(0)
        if symtab.is_methodname(varname,scope_stack[-1]):
            print("error: ",name," is already defined as method!")
            sys.exit(0)
        if symtab.is_classname(varname):
            print("error: ",name," is already defined as a class!")
            sys.exit(0)
        if is_attri:
            symtab.insertSymbol(id=varname,scope=scope_stack[-1],kind="attribute",type=current_type)
        else:
            symtab.insertSymbol(id=varname,scope=scope_stack[-1],kind="var",type=current_type)
        return

    #arg_list
    if node.nodeid == x_arg_list:
        if node.children[0].value == 'const':
            current_type = get_atype(node.children[1])
            varname = node.children[2].value
        else:
            current_type = get_atype(node.children[0])
            varname = node.children[1].value

        if symtab.is_methodname(varname,scope_stack[-2]):
            print("error: ",name," is already defined as method!")
            sys.exit(0)
        if symtab.is_classname(varname):
            print("error: ",name," is already defined as a class!")
            sys.exit(0)
        symtab.insertSymbol(id=varname,scope=scope_stack[-1],kind="arg",type=current_type)
        return
    
    #arg_list_tail
    if node.nodeid == x_arg_list_tail:
        if node.children[0].value == 'const':
            current_type = get_atype(node.children[1])
            varname = node.children[2].value
        else:
            current_type = get_atype(node.children[0])
            varname = node.children[1].value

        if symtab.is_methodname(varname,scope_stack[-2]):
            print("error: ",name," is already defined as method!")
            sys.exit(0)
        if symtab.is_classname(varname):
            print("error: ",name," is already defined as a class!")
            sys.exit(0)
        symtab.insertSymbol(id=varname,scope=scope_stack[-1],kind="arg",type=current_type)
        return
    
    #stm
    #stm -> [x_id] ustm
    if node.nodeid == x_stm:
        if node.children[0].nodeid == x_id:
            labelname = node.children[0].value
            if symtab.is_label(labelname,scope_stack[-1]):
                print("error: ",labelname," is already defined!")
                sys.exit(0)
            if symtab.is_classname(labelname):
                print("error: ",labelname," is already defined as classname!")
                sys.exit(0)
            symtab.insertSymbol(id=labelname,scope=scope_stack[-1],kind="label")
        return
    
    if node.nodeid == x_type:
        current_type = get_type(node)
        return


    ##check for the var is defined or not
    if node.nodeid == x_id or node.nodeid == x_var:
        if parent.nodeid == x_class_header or parent.nodeid == x_method_header:
            if not symtab_check(node.value,scope_stack[-2]):
                message = node.value+": invalid variable!"
                print('[line {}]'.format(node.pline),message)
                print("offending line:\n {",end='')
                show_line(node.pline)
                print('}')
                sys.exit(0)
        else:
            if not symtab_check(node.value,scope_stack[-1]):
                message = node.value+": invalid variable!"
                print('[line {}]'.format(node.pline),message)
                print("offending line:\n {",end='')
                show_line(node.pline)
                print('}')
                sys.exit(0)
        return
    
def seman(ptree,parent):
    global symtab
    global scope_stack

    sub_seman(ptree,parent)
    for i in ptree.children:
        seman(i,ptree)
    return symtab

def check_def(node):
    global scope_stack1
    global symtab
    #for checking the current scope
    if node.nodeid == x_compilation_unit:
        scope_stack1.append('global')
        return
    
    #endmain condition
    if node.nodeid == x_main_body:
        if node.leaf():
            scope_stack1.pop()
            return
    #main
    if node.nodeid == x_main_section:
        scope_stack1.append('main')
        return
    #class
    if node.nodeid == x_class_header:
        classname = node.children[0].value
        #new scope
        scope_stack1.append(classname)
        return
    
    #method
    if node.nodeid == x_method_header:
        name = node.children[1].value
        new_scope = scope_stack1[-1]+'.'+name
        scope_stack1.append(new_scope)
        return
    
    #endmethod condition
    if node.nodeid == x_method_body:
        if node.leaf():
            scope_stack1.pop()
            return
    #endclass condition
    if node.nodeid == x_class_body:
        if len(node.children) == 0:
            scope_stack1.pop()
            return

    if node.nodeid == x_id or node.nodeid == x_var:
        print(node.value)
        for i in range(len(scope_stack1)-1,-1,-1):
            if(symtab.find(node.value,scope_stack1[i])):
                break
        else:
            message = node.value+": variable not defined!"
            print('[line {}]'.format(node.pline),message)
            print("offending line:\n {",end='')
            show_line(node.pline)
            print('}')
            sys.exit(0)
    return 

def check_var_def(ptree):
    global scope_stack1
    check_def(ptree)
    for i in ptree.children:
        check_var_def(i)
    
    


        
        
