import ply.yacc as yacc
import pangulex
from ptree import *
from pangusem import *

import sys

y_data = ''
tokens = pangulex.tokens

precedence = (
    ('nonassoc', 'ASSIG', 'PASSIG'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIV', 'IDIV', 'MOD','AND', 'OR'),
    ('right', 'UMINUS', 'UNOT'))

y_show_productions = False
y_build_ptree = False
y_ptree = None
y_show_ptree = False
y_deparse_ptree = False
y_show_symbol_table = False
y_build_symbol_table = False

y_scope_stack = []
y_symbol_table = []

def p_compilation_unit(p):
    '''compilation_unit : sections main_section'''
    if y_show_productions:
        print('compilation_unit -> sections main_section')
    if y_build_ptree:
        global y_ptree
        y_ptree = Node(x_compilation_unit)
        y_ptree.cond_attach(p[1],p[2])
        if p[1].leaf():
            y_ptree.pline = p[2].pline
            y_ptree.ppos = p[2].ppos
#end p_compilation_unit


def p_main_section(p):
    '''main_section : MAIN COLON main_body'''
    if y_show_productions:
        print('main_section -> MAIN COLON main_body')
    p[0] = Node(x_main_section)
    if y_build_ptree:
        p[0].cond_attach(p[3])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_main_section


def p_main_body(p):
    '''main_body : stm main_body
                 | var_definition main_body
                 | ENDMAIN'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            if p[1].nodeid == x_stm:
                print("main_body -> stm main_body")
            else:
                print("main_body -> var_definition main_body")
        else:
            print("main_body -> ENDMAIN")
    p[0] = Node(x_main_body)
    if y_build_ptree:
        if a > 2:
            p[0].cond_attach(p[1],p[2])
            p[0].pline = p[0].children[0].pline
            p[0].ppos = p[0].children[0].ppos
        else:
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
#end p_main_body


def p_sections(p):
    '''sections : var_definition sections
                | class_definition sections
                | '''
    a = len(p)
    if y_show_productions:
        if a == 3:
            if p[1].nodeid == x_var_definition:
                print('sections -> var_definition sections')
            else:
                print('sections -> class_definition sections')
        else:
            print("sections -> epsilon")
    p[0] = Node(x_sections)
    if y_build_ptree:
        if a == 3:
            p[0].cond_attach(p[1],p[2])
            p[0].pline = p[0].children[0].pline
            p[0].ppos = p[0].children[0].ppos
#end p_sections


def p_var_definition(p):
    '''var_definition : type var_list
                      | PERMANENT type var_list
                      | CONST type var_list
                      | PERMANENT CONST type var_list
                      | CONST PERMANENT type var_list'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print('var_definition -> type var_list')
        elif a == 4:
            if p[1] == 'permanent':
                print('var_definition -> PERMANENT type var_list')
            else:
                print('var_definition -> CONST type var_list')
        else:
            if p[1] == 'permanent':
                print('var_definition -> PERMANENT CONST type var_list')
            else:
                print('var_definition -> CONST PERMANENT type var_list')
    p[0] = Node (x_var_definition)
    if y_build_ptree:
        if a == 3:
            p[0].attach(p[1],p[2])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        elif a == 4:
            if p[1] == 'permanent':
                t = Node(x_permanent)
                t.value = 'permanent'
                p[0].attach(t,p[2])
                p[0].cond_attach(p[3])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else:
                t = Node(x_const)
                t.value = 'const'
                p[0].attach(t,p[2])
                p[0].cond_attach(p[3])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
        else:
            t = Node(x_permanent_const) ##it should be fixed now, check it if possible
            if p[1] == 'permanent':
                t.value = 'permanent const'
            else:
                t.value = 'const permanent'
            p[0].attach(t,p[3])
            p[0].cond_attach(p[4])
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
#end p_var_definition


def p_class_definition(p):
    '''class_definition : CLASS class_header'''
    if y_show_productions:
        print('class_definition -> CLASS class_header')
    p[0] = Node(x_class_definition)
    if y_build_ptree:
        p[0].attach(p[2])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_class_definition


def p_class_header(p):
    '''class_header : ID_COLON class_body
                    | ID EXTENDS ID_COLON class_body'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print('class_header -> ID_COLON class_body')
        else:
            print('class_header -> ID EXTENDS ID_COLON class_body')
    if a == 3:
        xid = p[1][:-1]
    else:
        xid = p[1]
    p[0] = Node(x_class_header)
    if y_build_ptree:
        t = Node(x_id)
        t.value = xid
        p[0].attach(t)
        if a == 3:
            p[0].cond_attach(p[2])
        else:
            r = Node(x_id)
            r.value = p[3][:-1]
            p[0].attach(r)
            p[0].cond_attach(p[4])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_class_header


def p_var_list(p):
    '''var_list : ID SEMI
                | ID COMMA var_list_tail
                | ID ASSIG expression SEMI
                | ID ASSIG expression COMMA var_list_tail
                | ID PASSIG expression SEMI
                | ID PASSIG expression COMMA var_list_tail
                | ID PASSIG ALLOC ID_LP par_list SEMI
                | ID PASSIG ALLOC ID_LP par_list COMMA var_list_tail'''
    a = len(p)
    if p[1][-1] == ',':
        xid = p[1][:-1]
    else:
        xid = p[1]
    if y_show_productions:
        if a == 3:
            print('var_list -> ID SEMI')
        elif a == 4:
            print('var_list -> ID COMMA var_list_tail')
        elif a == 5:
            if p[2] == '=':
                print('var_list -> ID ASSIG expression SEMI')
            else:
                print('var_list -> ID PASSIG expression SEMI')
        elif a == 6:
            if p[2] == '=':
                print('var_list -> ID ASSIG expression COMMA var_list_tail')
            else:
                print('var_list -> ID PASSIG expression COMMA var_list_tail')
        elif a == 7:
            print('var_list -> ID PASSIG ALLOC ID_LP par_list SEMI')
        else: # a == 8
            print('var_list -> ID PASSIG ALLOC ID_LP par_list COMMA var_list_tail')
    p[0] = Node(x_var_list)
    if y_build_ptree:
        if a == 3:
            # var_list -> ID SEMI
            t = Node(x_id)
            t.value = p[1]
            p[0].attach(t)
        elif a == 4:
            # var_list -> ID COMMA var_list_tail
            t = Node(x_id)
            t.value = p[1]
            p[0].attach(t)
            p[0].cond_attach(p[3])
        elif a == 5:
            if p[2] == '=':
                # var_list -> ID ASSIG expression SEMI
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_assig)
                r.value = '='
                p[0].attach(t,r,p[3])
            else:
                # var_list -> ID PASSIG expression SEMI
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_passig)
                r.value = '@='
                p[0].attach(t,r,p[3])

        elif a == 6:
            if p[2] == '=':
                # var_list -> ID ASSIG expression COMMA var_list_tail
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_assig)
                r.value = '='
                p[0].attach(t,r,p[3],p[5])
            else:
                # var_list -> ID PASSIG expression COMMA var_list_tail
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_passig)
                r.value = '@='
                p[0].attach(t,r,p[3],p[5])
        elif a == 7:
            # var_list -> ID PASSIG ALLOC ID_LP par_list SEMI
            t = Node(x_id)
            t.value = p[1]
            r = Node(x_alloc)
            r.value = '@=alloc'
            s = Node(x_id)
            s.value = p[4][:-1]
            p[0].attach(t,r,s)
            p[0].cond_attach(p[5])
        else: # a == 8
            # var_list -> ID PASSIG ALLOC ID_LP par_list COMMA var_list_tail
            t = Node(x_id)
            t.value = p[1]
            r = Node(x_alloc)
            r.value = '@=alloc'
            s = Node(x_id)
            s.value = p[4][:-1]
            p[0].attach(t,r,s)
            p[0].cond_attach(p[5],p[7])
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_var_list


def p_var_list_tail(p):
    '''var_list_tail : ID SEMI
                     | ID COMMA var_list_tail
                     | ID ASSIG expression SEMI
                     | ID ASSIG expression COMMA var_list_tail
                     | ID PASSIG expression SEMI
                     | ID PASSIG expression COMMA var_list_tail
                     | ID PASSIG ALLOC ID_LP par_list SEMI
                     | ID PASSIG ALLOC ID_LP par_list COMMA var_list_tail'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print('var_list_tail -> ID SEMI')
        elif a == 4:
            print('var_list_tail -> ID COMMA var_list_tail')
        elif a == 5:
            if p[2] == '=':
                print('var_list_tail -> ID ASSIG expression SEMI')
            else:
                print('var_list_tail -> ID PASSIG expression SEMI')
        elif a == 6:
            if p[2] == '=':
                print('var_list_tail -> ID ASSIG expression COMMA var_list_tail')
            else:
                print('var_list_tail -> ID PASSIG expression COMMA var_list_tail')
        elif a == 7:
            print('var_list_tail -> ID PASSIG ALLOC ID_LP par_list SEMI')
        else: # a == 8
            print('var_list_tail -> ID PASSIG ALLOC ID_LP par_list COMMA var_list_tail')
    p[0] = Node(x_var_list_tail)
    if y_build_ptree:
        if a == 3:
            # var_list_tail -> ID SEMI
            t = Node(x_id)
            t.value = p[1]
            p[0].attach(t)
        elif a == 4:
            # var_list_tail -> ID COMMA var_list_tail
            t = Node(x_id)
            t.value = p[1]
            p[0].attach(t)
            p[0].cond_attach(p[3])
        elif a == 5:
            if p[2] == '=':
                # var_list_tail -> ID ASSIG expression SEMI
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_assig)
                r.value = '='
                p[0].attach(t,r,p[3])
            else:
                # var_list_tail -> ID PASSIG expression SEMI
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_passig)
                r.value = '@='
                p[0].attach(t,r,p[3])

        elif a == 6:
            if p[2] == '=':
                # var_list_tail -> ID ASSIG expression COMMA var_list_tail
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_assig)
                r.value = '='
                p[0].attach(t,r,p[3],p[5])
            else:
                # var_list_tail -> ID PASSIG expression COMMA var_list_tail
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_passig)
                r.value = '@='
                p[0].attach(t,r,p[3],p[5])
        elif a == 7:
            # var_list_tail -> ID PASSIG ALLOC ID_LP par_list SEMI
            t = Node(x_id)
            t.value = p[1]
            r = Node(x_alloc)
            r.value = '@= alloc'
            s = Node(x_id)
            s.value = p[4][:-1]
            p[0].attach(t,r,s)
            p[0].cond_attach(p[5])
        else: # a == 8
            # var_list_tail -> ID PASSIG ALLOC ID_LP par_list COMMA var_list_tail
            t = Node(x_id)
            t.value = p[1]
            r = Node(x_alloc)
            r.value = '@=alloc'
            s = Node(x_id)
            s.value = p[4][:-1]
            sys.exit(0)
            p[0].attach(t,r,s)
            p[0].cond_attach(p[5],p[7])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_var_list_tail



def p_type(p):
    '''type : BOOL
            | CHAR
            | STRING
            | INT
            | FLOAT
            | ID
            | BOOL_LS type_tail
            | CHAR_LS type_tail
            | STRING_LS type_tail
            | INT_LS type_tail
            | FLOAT_LS type_tail
            | ID_LS type_tail
            | FILE'''
    if y_show_productions:
        if p[1] == 'bool':
            print('type -> BOOL')
        elif p[1] == 'bool[':
            print('type -> BOOL_LS type_tail')
        elif p[1] == 'char':
            print('type -> CHAR')
        elif p[1] == 'char[':
            print('type -> CHAR_LS type_tail')
        elif p[1] == 'string':
            print('type -> STRING')
        elif p[1] == 'string[':
            print('type -> STRING_LS type_tail')
        elif p[1] == 'int':
            print('type -> INT')
        elif p[1] == 'int[':
            print('type -> INT_LS type_tail')
        elif p[1] == 'float':
            print('type -> FLOAT')
        elif p[1] == 'float[':
            print('type -> FLOAT_LS type_tail')
        elif p[1] == 'File':
            print('type -> FILE')
        else:
            if p[1][-1] == '[':
                print('type -> ID_LS type_tail')
            else:
                print('type -> ID')
    p[0] = Node(x_type)
    if y_build_ptree:
        if p[1] == 'bool':
            t = Node(x_bool)
            t.value = 'bool'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
        elif p[1] == 'bool[':
            t = Node(x_bool)
            t.value = 'bool'
            r = Node(x_dim)
            r.value = p[2]
            p[0].attach(t,r)
        elif p[1] == 'char':
            t = Node(x_char)
            t.value = 'char'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
        elif p[1] == 'char[':
            t = Node(x_char)
            t.value = 'char'
            r = Node(x_dim)
            r.value = p[2]
            p[0].attach(t,r)
        elif p[1] == 'string':
            t = Node(x_string)
            t.value = 'string'
            t.dim = 0
            p[0].attach(t)
        elif p[1] == 'string[':
            t = Node(x_string)
            t.value = 'string'
            r = Node(x_dim)
            r.value = p[2]
            p[0].attach(t,r)
        elif p[1] == 'int':
            t = Node(x_int)
            t.value = 'int'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
        elif p[1] == 'int[':
            t = Node(x_int)
            t.value = 'int'
            r = Node(x_dim)
            r.value = p[2]
            p[0].attach(t,r)
        elif p[1] == 'float':
            t = Node(x_float)
            t.value = 'float'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
        elif p[1] == 'float[':
            t = Node(x_float)
            t.value = 'float'
            r = Node(x_dim)
            r.value = p[2]
            p[0].attach(t,r)
        elif p[1] == 'File':
            t = Node(x_id)
            t.value = 'File'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
        else:
            if p[1][-1] == '[':
                t = Node(x_id)
                t.value = p[1][:-1]
                r = Node(x_dim)
                r.value = p[2]
                p[0].attach(t,r)
            else:
                t = Node(x_id)
                t.value = p[1]
                r = Node(x_dim)
                r.value = 0
                p[0].attach(t,r)
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_type



def p_type_tail(p):
    '''type_tail : RLS type_tail
                 | RS'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print("type_tail -> RLS type_tail")
        else:
            print("type_tail -> RS")
    # do not build any node for this one
    if a == 3:
        p[0] = p[2]+1
    else:
        p[0] = 1
#end p_type_tail


def p_atype(p):
    '''atype : BOOL
             | CHAR
             | STRING
             | INT
             | FLOAT
             | ID
             | BOOL_AT
             | CHAR_AT
             | STRING_AT
             | INT_AT
             | FLOAT_AT
             | ID_AT
             | BOOL_LS atype_tail
             | CHAR_LS atype_tail
             | STRING_LS atype_tail
             | INT_LS atype_tail
             | FLOAT_LS atype_tail
             | ID_LS atype_tail
             | FILE'''
    a = len(p)
    if y_show_productions:
        if p[1] == 'bool':
            print('atype -> BOOL')
        elif p[1] == 'bool&':
            print('atype -> BOOL_AT')
        elif p[1] == 'bool[':
            print('atype -> BOOL_LS atype_tail')
        elif p[1] == 'char':
            print('atype -> CHAR')
        elif p[1] == 'char&':
            print('atype -> CHAR_AT')
        elif p[1] == 'char[':
            print('atype -> CHAR_LS atype_tail')
        elif p[1] == 'string':
            print('atype -> STRING')
        elif p[1] == 'string&':
            print('atype -> STRING_AT')
        elif p[1] == 'string[':
            print('atype -> STRING_LS atype_tail')
        elif p[1] == 'int':
            print('atype -> INT')
        elif p[1] == 'int&':
            print('atype -> INT_AT')
        elif p[1] == 'int[':
            print('atype -> INT_LS atype_tail')
        elif p[1] == 'float':
            print('atype -> FLOAT')
        elif p[1] == 'float&':
            print('atype -> FLOAT_AT')
        elif p[1] == 'float[':
            print('atype -> FLOAT_LS atype_tail')
        elif p[1] == 'File':
            print('atype -> FILE')
        else:
            if a == 2:
                if p[1][-1] == '&':
                    print('atype -> ID_AT')
                else:
                    print('atype -> ID')
            else:
                print('atype -> ID_LS atype_tail')
    p[0] = Node(x_atype)
    if y_build_ptree:
        # bool
        if p[1] == 'bool':
            t = Node(x_bool)
            t.value = 'bool'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'bool&':
            t = Node(x_bool)
            t.value = 'bool'
            r = Node(x_dim)
            r.value = 0
            s = Node(x_at)
            s.value = '&'
            p[0].attach(t,r,s)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'bool[':
            t = Node(x_bool)
            t.value = 'bool'
            r = Node(x_dim)
            r.value = p[2][0]
            if p[2][1]:
                s = Node(x_at)
                s.value = '&'
                p[0].attach(t,r,s)
            else:
                p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        # char
        elif p[1] == 'char':
            t = Node(x_char)
            t.value = 'char'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'char&':
            t = Node(x_char)
            t.value = 'char'
            r = Node(x_dim)
            r.value = 0
            s = Node(x_at)
            s.value = '&'
            p[0].attach(t,r,s)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'char[':
            t = Node(x_char)
            t.value = 'char'
            r = Node(x_dim)
            r.value = p[2][0]
            if p[2][1]:
                s = Node(x_at)
                s.value = '&'
                p[0].attach(t,r,s)
            else:
                p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        # string
        elif p[1] == 'string':
            t = Node(x_string)
            t.value = 'string'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'string&':
            t = Node(x_string)
            t.value = 'string'
            r = Node(x_dim)
            r.value = 0
            s = Node(x_at)
            s.value = '&'
            p[0].attach(t,r,s)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'string[':
            t = Node(x_string)
            t.value = 'string'
            r = Node(x_dim)
            r.value = p[2][0]
            if p[2][1]:
                s = Node(x_at)
                s.value = '&'
                p[0].attach(t,r,s)
            else:
                p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        # int
        elif p[1] == 'int':
            t = Node(x_int)
            t.value = 'int'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'int&':
            t = Node(x_int)
            t.value = 'int'
            r = Node(x_dim)
            r.value = 0
            s = Node(x_at)
            s.value = '&'
            p[0].attach(t,r,s)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'int[':
            t = Node(x_int)
            t.value = 'int'
            r = Node(x_dim)
            r.value = p[2][0]
            if p[2][1]:
                s = Node(x_at)
                s.value = '&'
                p[0].attach(t,r,s)
            else:
                p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        # float
        elif p[1] == 'float':
            t = Node(x_float)
            t.value = 'float'
            r = Node(x_dim)
            r.value = 0
            p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'float&':
            t = Node(x_float)
            t.value = 'float'
            r = Node(x_dim)
            r.value = 0
            s = Node(x_at)
            s.value = '&'
            p[0].attach(t,r,s)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'float[':
            t = Node(x_float)
            t.value = 'float'
            r = Node(x_dim)
            r.value = p[2][0]
            if p[2][1]:
                s = Node(x_at)
                s.value = '&'
                p[0].attach(t,r,s)
            else:
                p[0].attach(t,r)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif p[1] == 'File':
            t = Node(x_file)
            t.value = 'File'
            p[0].attach(t)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        else:
            if a == 2:
                if p[1][-1] == '&':
                    t = Node(x_id)
                    t.value = p[1][:-1]
                    r = Node(x_dim)
                    r.value = 0
                    s = Node(x_at)
                    s.value = '&'
                    p[0].attach(t,r,s)
                    p[0].pline = pline(p,1)
                    p[0].ppos = ppos(p,1)
                else:
                    t = Node(x_id)
                    t.value = p[1]
                    r = Node(x_dim)
                    r.value = 0
                    p[0].attach(t,r)
                    p[0].pline = pline(p,1)
                    p[0].ppos = ppos(p,1)
            else:
                t = Node(x_id)
                t.value = p[1][:-1]
                r = Node(x_dim)
                r.value = p[2][0]
                if p[2][1]:
                    s = Node(x_at)
                    s.value = '&'
                    p[0].attach(t,r,s)
                    p[0].pline = pline(p,1)
                    p[0].ppos = ppos(p,1)
                else:
                    p[0].attach(t,r)
                    p[0].pline = pline(p,1)
                    p[0].ppos = ppos(p,1)
#end p_atype



def p_atype_tail(p):
    '''atype_tail : RLS atype_tail
                  | RS_AT
                  | RS'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print("atype_tail -> RLS atype_tail")
        else:
            if p[1][-1] == '&':
                print('atype -> RS_AT')
            else:
                print("atype_tail -> RS")
    # do not build any node for this one
    if a == 3:
        # p[3] is a pair [dim,at]
        p[0] = [p[2][0]+1,p[2][1]]
    else:
        if p[1][-1] == '&':
            p[0] = [1,True]
        else:
            p[0] = [1,False]
#end p_atype_tail

def p_stms(p):
    '''stms : stm stms
            | stm'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print("stms -> stm stms")
        else:
            print("stms -> stm")
    p[0] = Node(x_stms)
    if y_build_ptree:
        if a == 3:
            p[0].cond_attach(p[1],p[2])
        else:
            p[0].attach(p[1])
        p[0].pline = p[1].pline
        p[0].ppos = p[1].ppos
#end p_stms


def p_stm(p):
    ''' stm : ID_COLON ustm
            | ustm'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print('stm -> ID_COLON ustm')
        else:
            print('stm -> ustm')
    p[0] = Node(x_stm)
    if a == 3:
        if p[2].nodeid == x_goto_stm:
            if p[2].value == p[1][:-1]:
                syn_error("looping goto statemen",p)
    if y_build_ptree:
        if a == 3:
            t = Node(x_id)
            t.value = p[1][:-1]
            p[0].attach(t,p[2])
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        else:
            p[0].attach(p[1])
            p[0].pline = p[1].pline
            p[0].ppos = p[0].ppos
#end p_stm


def p_class_body(p):
    '''class_body : ENDCLASS
                  | attr_definition class_body
                  | method_header method_body class_body
                  | PUBLIC method_header method_body class_body
                  | PRIVATE method_header method_body class_body'''
    a = len(p)
    if y_show_productions:
        if a == 2:
            print('class_body -> ENDCLASS')
        elif a == 3:
            print('class_body -> attr_definition class_body')
        elif a == 4:
            print('class_body -> method_header method_body class_body')
        else:
            if p[1] == 'public':
                print('class_body -> PUBLIC method_header method_body class body')
            else:
                print('class_body -> PRIVATE method_header method_body class body')
    p[0] = Node(x_class_body)
    if y_build_ptree:
        if a == 2:
            # class_body -> ENDCLASS
            return
        elif a == 3:
            # class_body -> attr_definition class_body
            p[0].attach(p[1],p[2]) ## should include p[2] for popping the scope
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        elif a == 4: ##!!! dont know how to
            # class_body -> method_header method_body class_body
            t = Node(x_public)
            t.value = 'public'
            p[1].prettach(t)  # make the method header public
            s = Node(x_method_definition)
            s.attach(p[1])
            s.cond_attach(p[2]) # method_definition = method_header+method_body
            p[0].attach(s)
            p[0].attach(s,p[3])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        else:
            if p[1] == 'public':
                # class_body -> PUBLIC method_header method_body class body
                t = Node(x_public)
                t.value = 'public'
                p[2].prettach(t)  # make the method header public
                s = Node(x_method_definition)
                s.attach(p[2])
                s.cond_attach(p[3]) # method_definition = method_header+method_body
                p[0].attach(s,p[4])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else:
                # class_body -> PRIVATE method_header method_body class body
                t = Node(x_private)
                t.value = 'private'
                p[2].prettach(t)  # make the method header private
                s = Node(x_method_definition)
                s.attach(p[2])
                s.cond_attach(p[3]) # method_definition = method_header+method_body
                p[0].attach(s,p[4])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
#end class_body


def p_attr_definition(p):
    '''attr_definition : PUBLIC SHARED CONST type var_list
                       | PUBLIC CONST SHARED type var_list
                       | PRIVATE SHARED CONST type var_list
                       | PRIVATE CONST SHARED type var_list
                       | PUBLIC SHARED type var_list
                       | PUBLIC CONST type var_list
                       | SHARED CONST type var_list
                       | CONST SHARED type var_list
                       | PRIVATE SHARED type var_list
                       | PRIVATE CONST type var_list
                       | PUBLIC type var_list
                       | SHARED type var_list
                       | CONST type var_list
                       | PRIVATE type var_list
                       | type var_list'''
    a = len(p)
    if y_show_productions:
        if a == 6:
            if p[1]=='public' and p[2]=='shared' and p[3]=='const':
                print('attr_definition -> PUBLIC SHARED CONST type var_list')
            elif p[1]=='public' and p[2]=='const' and p[3]=='shared':
                print('attr_definition -> PUBLIC CONST SHARED type var_list')
            elif p[1]=='private' and p[2]=='shared' and p[3]=='const':
                print('attr_definition -> PRIVATE SHARED CONST type var_list')
            else: # p[1]=='private' and p[2]=='const' and p[3]=='shared':
                print('attr_definition -> PRIVATE CONST SHARED type var_list')
        elif a == 5:
            if p[1]=='public' and p[2]=='shared':
                print('attr_definition -> PUBLIC SHARED type var_list')
            elif p[1]=='public' and p[2]=='const':
                print('attr_definition -> PUBLIC CONST type var_list')
            elif p[1]=='shared' and p[2]=='const':
                print('attr_definition -> SHARED CONST type var_list')
            elif p[1]=='const' and p[2]=='shared':
                print('attr_definition -> CONST SHARED type var_list')
            elif p[1]=='private' and p[2]=='shared':
                print('attr_definition -> PRIVATE SHARED type var_list')
            else: # p[1]=='private' and p[2]=='const':
                print('attr_definition -> PRIVATE CONST type var_list')
        elif a == 4:
            if p[1]=='public':
                print('attr_definition -> PUBLIC type var_list')
            elif p[1]=='shared':
                print('attr_definition ->  SHARED type var_list')
            elif p[1]=='const':
                print('attr_definition -> CONST type var_list')
            else: # if p[1]=='private':
                print('attr_definition ->  PRIVATE type var_list')
        else:
             print('attr_definition -> type var_list')
    p[0] = Node(x_attr_definition)
    if y_build_ptree:
        if a == 6:
            if p[1]=='public' and p[2]=='shared' and p[3]=='const':
                t = Node(x_public_shared_const)
                t.value = "public shared const"
                p[0].attach(t)
                p[0].cond_attach(p[4],p[5])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1]=='public' and p[2]=='const' and p[3]=='shared':
                t = Node(x_public_shared_const)
                t.value = "public const shared"###fixed
                p[0].attach(t)
                p[0].cond_attach(p[4],p[5])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1]=='private' and p[2]=='shared' and p[3]=='const':
                t = Node(x_private_shared_const)###change to x_private_shared_const?
                t.value = "private shared const"###fixed
                p[0].attach(t)
                p[0].cond_attach(p[4],p[5])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else: # p[1]=='private' and p[2]=='const' and p[3]=='shared':
                t = Node(x_private_shared_const)###change to x_private_shared_const?
                t.value = "private const shared"###fixed
                p[0].attach(t)
                p[0].cond_attach(p[4],p[5])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
        elif a == 5:
            if p[1]=='public' and p[2]=='shared':
                t = Node(x_public_shared)
                t.value = "public shared"
                p[0].attach(t)
                p[0].cond_attach(p[3],p[4])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1]=='public' and p[2]=='const':
                t = Node(x_public_const)
                t.value = "public const"
                p[0].attach(t)
                p[0].cond_attach(p[3],p[4])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1]=='shared' and p[2]=='const':
                t = Node(x_shared_const)
                t.value = "shared const"
                p[0].attach(t)
                p[0].cond_attach(p[3],p[4])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1]=='const' and p[2]=='shared':
                t = Node(x_shared_const)
                t.value = "const shared" ###fixed
                p[0].attach(t)
                p[0].cond_attach(p[3],p[4])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1]=='private' and p[2]=='shared':
                t = Node(x_private_shared)
                t.value = "private shared"
                p[0].attach(t)
                p[0].cond_attach(p[3],p[4])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else: # p[1]=='private' and p[2]=='const':
                t = Node(x_private_const)
                t.value = "private const"
                p[0].attach(t)
                p[0].cond_attach(p[3],p[4])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
        elif a == 4:
            if p[1]=='public':
                t = Node(x_public)
                t.value = "public"
                p[0].attach(t)
                p[0].cond_attach(p[2],p[3])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1]=='shared':
                t = Node(x_shared)
                t.value = "shared"
                p[0].attach(t)
                p[0].cond_attach(p[2],p[3])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1]=='const':
                t = Node(x_const)
                t.value = 'const'
                p[0].attach(t)
                p[0].cond_attach(p[2],p[3])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else: # if p[1]=='private':
                t = Node(x_private)
                t.value = 'private'
                p[0].attach(t)
                p[0].cond_attach(p[2],p[3])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
        else:### attr_definition -> type var_list
            p[0].cond_attach(p[1],p[2])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
#end attr_definition


def p_method_header(p):
    '''method_header : METHOD ID_LP arg_list ARROW type COLON
                     | METHOD ID_LP arg_list COLON'''
    a = len(p)
    if y_show_productions:
        if a == 5:
            print('method_header -> METHOD ID_LP arg_list COLON')
        else:
            print('method_header -> METHOD ID_LP arg_list ARROW type COLON')
    p[0] = Node(x_method_header)
    if y_build_ptree:
        if a == 5:
            t = Node(x_id)
            t.value = p[2][:-1]
            p[0].attach(t)
            p[0].attach(p[3])
        else:
            t = Node(x_id)
            t.value = p[2][:-1]
            p[0].attach(t)
            p[0].cond_attach(p[3],p[5])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_method_header


def p_arg_list(p):
    '''arg_list : RP
                | atype ID RP
                | atype ID COMMA arg_list_tail
                | CONST atype ID RP
                | CONST atype ID COMMA arg_list_tail'''
    a = len(p)
    if y_show_productions:
        if a == 2:
            print('arg_list -> RP')
        elif a == 4:
            print('arg_list -> atype ID RP')
        elif a == 5:
            if p[3] == ',':
                print('arg_list -> atype ID COMMA arg_list_tail')
            else:
                print('arg_list -> CONST atype ID RP')
        else:
            print('arg_list -> CONST atype ID COMMA arg_list_tail')
    p[0] = Node(x_arg_list)
    if y_build_ptree:
        if a == 2:
            # arg_list -> RP
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif a == 4:
            # arg_list -> atype ID RP
            t = Node(x_id)
            t.value = p[2]
            p[0].attach(p[1],t)
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        elif a == 5:
            if p[3] == ',':
                # arg_list -> atype ID COMMA arg_list_tail
                t = Node(x_id)
                t.value = p[2]
                p[0].attach(p[1],t,p[4])
                p[0].pline = p[1].pline
                p[0].ppos = p[1].ppos
            else:
                # arg_list -> CONST atype ID RP
                t = Node(x_const)
                t.value = p[1]
                r = Node(x_id)
                r.value = p[3]
                p[0].attach(t,p[2],r)
                p[0].pline = p[2].pline#original one is p[0].pline = p[1].pline but error!
                p[0].ppos = p[2].ppos#
        else:
            # arg_list -> CONST atype ID COMMA arg_list_tail
            t = Node(x_const)
            t.value = p[1]
            r = Node(x_id)
            r.value = p[3]
            p[0].attach(t,p[2],r,p[5])
            p[0].pline = p[2].pline#original one is p[0].pline = p[1].pline but error!
            p[0].ppos = p[2].ppos##
#end p_arg_list


def p_arg_list_tail(p):
    '''arg_list_tail : RP
                     | atype ID RP
                     | atype ID COMMA arg_list_tail
                     | CONST atype ID RP
                     | CONST atype ID COMMA arg_list_tail'''
    a = len(p)
    if y_show_productions:
        if a == 2:
            print('arg_list -> RP')
        elif a == 4:
            print('arg_list -> atype ID RP')
        elif a == 5:
            if p[3] == ',':
                print('arg_list -> atype ID COMMA arg_list_tail')
            else:
                print('arg_list -> CONST atype ID RP')
        else:
            print('arg_list -> CONST atype ID COMMA arg_list_tail')
    p[0] = Node(x_arg_list_tail)
    if y_build_ptree:
        if a == 2:
            # arg_list_tail -> RP
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif a == 4:
            # arg_list_tail -> atype ID RP
            t = Node(x_id)
            t.value = p[2]
            p[0].attach(p[1],t)
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        elif a == 5:
            if p[3] == ',':
                # arg_list_tail -> atype ID COMMA arg_list_tail
                t = Node(x_id)
                t.value = p[2]
                p[0].attach(p[1],t,p[4])
                p[0].pline = p[1].pline
                p[0].ppos = p[1].ppos
            else:
                # arg_list_tail -> CONST atype ID RP
                t = Node(x_const)
                t.value = p[1]
                r = Node(x_id)
                r.value = p[3]
                p[0].attach(t,p[2],r)
                p[0].pline = p[2].pline### orginal one is
                p[0].ppos = p[2].ppos###
        else:
            # arg_list_tail -> CONST atype ID COMMA arg_list_tail
            t = Node(x_const)
            t.value = p[1]
            r = Node(x_id)
            r.value = p[3]
            p[0].attach(t,p[2],r,p[5])
            p[0].pline = p[2].pline###
            p[0].ppos = p[2].ppos###
#end p_arg_list_tail



def p_method_body(p):
    '''method_body : stm method_body
                   | var_definition method_body
                   | ENDMETHOD'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            if p[1].nodeid == x_var_definition:
                print('method_body -> stm method_body')
            else:
                print('method_body -> var_definition method_body')
        else:
            print('method_body -> ENDMETHOD')
    p[0] = Node(x_method_body)
    if y_build_ptree:
        if a == 3:
            p[0].attach(p[1],p[2])##
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
#end p_method_body


def p_ustm(p):
    ''' ustm : null_stm
             | assig_stm
             | passig_stm
             | return_stm
             | preturn_stm
             | call_stm
             | if_stm
             | while_stm
             | for_stm
             | goto_stm
             | break_stm
             | continue_stm
             | guard_stm
             | raise_stm
             | terminate_stm'''
    if y_show_productions:
        if p[1].nodeid == x_assig_stm:
            print("ustm -> assig_stm")
        elif p[1].nodeid == x_passig_stm:
            print("ustm -> passig_stm")
        elif p[1].nodeid == x_return_stm:
            print("ustm -> return_stm")
        elif p[1].nodeid == x_preturn_stm:
            print("ustm -> preturn_stm")
        elif p[1].nodeid == x_call_stm:
            print("ustm -> call_stm")
        elif p[1].nodeid == x_if_stm:
            print("ustm -> if_stm")
        elif p[1].nodeid == x_while_stm:
            print("ustm -> while_stm")
        elif p[1].nodeid == x_for_stm:
            print("ustm -> for_stm")
        elif p[1].nodeid == x_goto_stm:
            print("ustm -> goto_stm")
        elif p[1].nodeid == x_null_stm:
            print("ustm -> null_stm")
        elif p[1].nodeid == x_break_stm:
            print('ustm -> break_stm')
        elif p[1].nodeid == x_continue_stm:
            print('ustm -> continue_stm')
        elif p[1].nodeid == x_guard_stm:
            print('ustm -> guard_stm')
        elif p[1].nodeid == x_raise_stm:
            print('ustm -> raise_stm')
        else:
            print('ustm -> terminate_stm')
    p[0] = p[1]
#end p_ustm



def p_break_stm(p):
    '''break_stm : BREAK SEMI'''
    if y_show_productions:
        print('break_stm -> BREAK SEMI')
    p[0] = Node(x_break_stm)
    if y_build_ptree:
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_break_stm


def p_continue_stm(p):
    '''continue_stm : CONTINUE SEMI'''
    if y_show_productions:
        print('continue_stm -> CONTINUE SEMI')
    p[0] = Node(x_continue_stm)
    if y_build_ptree:
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_continue_stm


def p_terminate_stm(p):
    '''terminate_stm : TERMINATE SEMI'''
    if y_show_productions:
        print('termiante_stm -> TERMINATE SEMI')
    p[0] = Node(x_terminate_stm)
    if y_build_ptree:
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_terminate_stm


def p_null_stm(p):
    '''null_stm : SEMI'''
    if y_show_productions:
        print('null_stm -> SEMI')
    p[0] = Node(x_null_stm)
    if y_build_ptree:
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_null_stm


def p_assig_stm(p):
    ''' assig_stm : storage ASSIG expression SEMI'''
    if y_show_productions:
        print('assig_stm -> storage ASSIG expression SEMI')
    p[0] = Node(x_assig_stm)
    if y_build_ptree:
        p[0].attach(p[1],p[3])
        p[0].pline = p[1].pline
        p[0].ppos = p[1].ppos
#end p_assig_stm


def p_passig_stm(p):
    ''' passig_stm : storage PASSIG expression SEMI
                   | storage PASSIG ALLOC ID_LP par_list SEMI'''
    a = len(p)
    if y_show_productions:
        if a == 5:
            print('passig_stm -> storage PASSIG expression SEMI')
        else:
            print('passig_stm -> storage PASSIG ALLOC ID_LP par_list SEMI')
    p[0] = Node(x_passig_stm)
    if y_build_ptree:
        if a == 5:
            # passig_stm -> storage PASSIG expression SEMI
            p[0].attach(p[1],p[3])
        else:
            # passig_stm -> storage PASSIG ALLOC ID_LP par_list SEMI
            t = Node(x_alloc)
            t.value = '@= alloc'
            s = Node(x_id)
            s.value = p[4][:-1]
            p[0].attach(p[1],t,s,p[5])
        p[0].pline = p[1].pline
        p[0].ppos = p[1].ppos
#end p_passig_stm


def p_call_stm(p):
    ''' call_stm : call SEMI'''
    if y_show_productions:
        print('call_stm -> call SEMI')
    p[0] = Node(x_call_stm)
    if y_build_ptree:
        p[0].attach(p[1])
    p[0].pline = p[1].pline
    p[0].ppos = p[1].ppos
#end p_call_stm


def p_if_stm(p):
    '''if_stm : IF expression THEN stms ENDIF
              | IF expression THEN stms ELSE stms ENDIF'''
    a = len(p)
    if y_show_productions:
        if a == 6:
            print("if_stm -> IF expression THEN stms ENDIF")
        else:
            print("if_stm -> IF expression THEN stms ELSE stms ENDIF")
    p[0] = Node(x_if_stm)
    if y_build_ptree:
        if a == 6:
            # if_stm -> IF expression THEN stms ENDIF
            p[0].attach(p[2])
            p[0].cond_attach(p[4])
        else:
            # if_stm -> IF expression THEN stms ELSE stms ENDIF
            p[0].attach(p[2])
            p[0].cond_attach(p[4],p[6])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_if_stm



def p_while_stm(p):
    ''' while_stm : WHILE expression DO stms ENDWHILE
                  | WHILE expression DO ENDWHILE
                  | WHILE DO stms ENDWHILE
                  | WHILE DO ENDWHILE'''
    a = len(p)
    if y_show_productions:
        if a == 6:
            print('while_stm -> WHILE expression DO stms ENDWHILE')
        elif a == 5:
            if p[2] == 'do':
                print('while_stm -> WHILE DO stms ENDWHILE')
            else:
                print('while_stm -> WHILE expression DO ENDWHILE')
        else:
            print("while_stm -> WHILE DO ENDWHILE")
    if a == 4:
        syn_warning("the while statement has no effect",p)
    p[0] = Node(x_while_stm)
    if y_build_ptree:
        if a == 6:
            #while_stm -> WHILE expression DO stms ENDWHILE
            p[0].attach(p[2],p[4])
        elif a == 5:
            if p[2] == 'do':
                # while_stm -> WHILE DO stms ENDWHILE
                p[0].attach(p[3])
            else:
                # while_stm -> WHILE expression DO ENDWHILE
                p[0].attach(p[2])
        else:
            #while_stm -> WHILE DO ENDWHILE
            pass
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_while_stm


def p_for_stm(p):
    '''for_stm : FOR prologue condition epilogue stms ENDFOR
               | FOR prologue condition epilogue ENDFOR'''
    a = len(p)
    if y_show_productions:
        if a == 7:
            print('for_stm -> FOR prologue condition epilogue stms ENDFOR')
        else:
            print('for_stm -> FOR prologue condition epilogue ENDFOR')
    p[0] = Node(x_for_stm)
    if y_build_ptree:
        if a == 7:
            p[0].cond_attach(p[2],p[3],p[4],p[5])
        else:
            p[0].cond_attach(p[2],p[3],p[4])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
        if len(p[0].children) == 0:
            syn_warning("the for statement has no effect",p)
#end p_for_stm


def p_goto_stm(p):
    '''goto_stm : GOTO ID SEMI'''
    if y_show_productions:
        print('goto_stm -> GOTO ID SEMI')
    p[0] = Node(x_goto_stm)
    if y_build_ptree:
        p[0].value = p[2]
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_goto_stm


def p_prologue(p):
    ''' prologue : storage ASSIG expression prologue_tail
                 | SEMI'''
    a = len(p)
    if y_show_productions:
        if a == 5:
            print('prologue -> storage ASSIG expression prologue_tail')
        else:
            print('prologue -> SEMI')
    p[0] = Node(x_prologue)
    if y_build_ptree:
        if a == 5:
            # prologue -> storage ASSIG expression prologue_tail
            t = Node(x_assig)
            t.value = "="
            p[0].attach(p[1],t,p[3])
            p[0].cond_attach(p[4])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        else:
            # prologue -> SEMI
            return
#end p_prologue



def p_prologue_tail(p):
    '''prologue_tail : COMMA storage ASSIG expression prologue_tail
                     | SEMI'''
    a = len(p)
    if y_show_productions:
        if a == 6:
            print('prologue_tail -> COMMA storage ASSIG expression prologue_tail')
        else:
            print('prologue_tail -> SEMI')
    p[0] = Node(x_prologue_tail)
    if y_build_ptree:
        if a == 6:
            # prologue_tail -> COMMA storage ASSIG expression prologue_tail
            t = Node(x_assig)
            t.value = "="
            p[0].attach(p[2],t,p[4])
            p[0].cond_attach(p[5])
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        else:
            # prologue_tail -> SEMI
            return
#end p_prologue_tail



def p_condition(p):
    '''condition : expression SEMI
                 | SEMI '''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print('condition -> expression SEMI')
        else:
            print('condition -> SEMI')
    p[0] = Node(x_condition)
    if y_build_ptree:
        if a == 3:
            # condition -> expression SEMI
            p[0].attach(p[1])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        else:
            # condition -> SEMI
            return
#end p_condition


def p_epilogue(p):
    '''epilogue : storage ASSIG expression epilogue_tail
                | DO'''
    a = len(p)
    if y_show_productions:
        if a == 5:
            print('epilogue -> storage ASSIG expression epilogue_tail')
        else:
            print('epilogue -> DO')
    p[0] = Node(x_epilogue)
    if y_build_ptree:
        if a == 5:
            # epilogue -> storage ASSIG expression epilogue_tail
            t = Node(x_assig)
            t.value = "="
            p[0].attach(p[1],t,p[3])
            p[0].cond_attach(p[4])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        else:
            # epilogue -> DO
            return
#end p_epilogue


def p_epilogue_tail(p):
    '''epilogue_tail : COMMA storage ASSIG expression epilogue_tail
                     | DO'''
    a = len(p)
    if y_show_productions:
        if a == 6:
            print('epilogue_tail -> COMMA storage ASSIG expression epilogue_tail')
        else:
            print('epilogue_tail -> DO')
    p[0] = Node(x_epilogue_tail)
    if a == 6:
        # epilogue_tail -> COMMA storage ASSIG expression epilogue_tail
        t = Node(x_assig)
        t.value = "="
        p[0].attach(p[2],t,p[4])
        p[0].cond_attach(p[5])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
    else:
        # epilogue_tail -> DO
        return
#end p_epilogue_tail


def p_storage(p):
    ''' storage : arr
                | var'''
    if y_show_productions:
        if p[1].nodeid == x_arr or p[1].nodeid == x_substr:
            print('storage -> arr')
        elif p[1].nodeid == x_var:
            print('storage -> var')
    p[0] = p[1]
#end p_storage


def p_return_stm(p):
    ''' return_stm : RETURN SEMI
                   | RETURN expression SEMI'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print("return_stm -> RETURN SEMI")
        else:
            print("return_stm -> RETURN expression SEMI")
    p[0] = Node(x_return_stm)
    if y_build_ptree:
        if a == 3:
            # return_stm -> RETURN SEMI
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
            return
        else:
            # return_stm -> RETURN expression SEMI
            p[0].attach(p[2])
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
#end p_return_stm


def p_preturn_stm(p):
    ''' preturn_stm : PRETURN expression SEMI'''
    if y_show_productions:
        print("return_stm -> PRETURN expression SEMI")
    p[0] = Node(x_preturn_stm)
    if y_build_ptree:
        p[0].attach(p[2])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_preturn_stm


def p_guard_stm(p):
    '''guard_stm : GUARD COLON stms CATCH COLON catch_block'''
    if y_show_productions:
        print('guard_stm -> GUARD COLON stms CATCH COLON catch_block')
    p[0] = Node(x_guard_stm)
    if y_build_ptree:
        p[0].cond_attach(p[3],p[6])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_guard_stm


def p_catch_block(p):
    '''catch_block : STRING_LIT COLON stms catch_block_tail'''
    if y_show_productions:
        print('catch_block -> STRING_LIT COLON stms catch_block_tail')
    p[0] = Node(x_catch_block)
    if y_build_ptree:
        t = Node(x_catch_label)
        t.value = p[1]
        p[0].attach(t)
        p[0].cond_attach(p[3],p[4])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_catch_block


def p_catch_block_tail(p):
    '''catch_block_tail : ENDCATCH
                        | STRING_LIT COLON stms catch_block_tail'''
    a = len(p)
    if y_show_productions:
        if a == 2:
            print('catch_block_tail -> ENDCATCH')
        else:
            print('catch_block_tail -> STRING_LIT COLON stms catch_block_tail')
    p[0] = Node(x_catch_block)
    if y_build_ptree:
        if a == 2:
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
            return
        else:
            t = Node(x_catch_label)
            t.value = p[1]
            p[0].attach(t)
            p[0].cond_attach(p[3],p[4])
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
#end p_catch_block_tail



def p_raise_stm(p):
    '''raise_stm : RAISE expression SEMI'''
    if y_show_productions:
        print('raise_stm -> RAISE expression SEMI')
    p[0] = Node(x_raise_stm)
    if y_build_ptree:
        p[0].attach(p[2])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_raise_stm


def p_expression(p):
    '''expression : simple_expression
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression STAR expression
                  | expression DIV expression
                  | expression IDIV expression
                  | expression MOD expression
                  | expression AND expression
                  | expression OR expression
                  | expression LT expression
                  | expression LE expression
                  | expression GT expression
                  | expression GE expression
                  | expression EQ expression
                  | expression NEQ expression'''
    a = len(p)
    if y_show_productions:
        if a == 2:
            print('expression -> simple_expression')
        else:
            if p[2] == '+':
                print('expression -> expression PLUS expression')
            elif p[2] == '-':
                print('expression -> expression MINUS expression')
            elif p[2] == '*':
                print('expression -> expression STAR expression')
            elif p[2] == '/':
                print('expression -> expression DIV expression')
            elif p[2] == '//':
                print('expression -> expression IDIV expression')
            elif p[2] == 'mod':
                print('expression -> expression MOD expression')
            elif p[2] == 'and':
                print('expression -> expression AND expression')
            elif p[2] == 'or':
                print('expression -> expression OR expression')
            elif p[2] == '<':
                print('expression -> expression LT expression')
            elif p[2] == '<=':
                print('expression -> expression LE expression')
            elif p[2] == '>':
                print('expression -> expression GT expression')
            elif p[2] == '>=':
                print('expression -> expression GE expression')
            elif p[2] == '==':
                print('expression -> expression EQ expression')
            else:
                print('expression -> expression NEQ expression')
    p[0] = Node(x_expression)
    if y_build_ptree:
        if a == 2:
            # expression -> simple_expression
            p[0] = p[1]
            return
        else:
            if p[2] == '+':
                #end expression -> expression PLUS expression
                t = Node(x_plus)
            elif p[2] == '-':
                #end expression -> expression MINUS expression
                t = Node(x_minus)
            elif p[2] == '*':
                #end expression -> expression STAR expression
                t = Node(x_star)
            elif p[2] == '/':
                #end expression -> expression DIV expression
                t = Node(x_div)
            elif p[2] == '//':
                #end expression -> expression IDIV expression
                t = Node(x_idiv)
            elif p[2] == 'mod':
                #end expression -> expression MOD expression
                t = Node(x_mod)
            elif p[2] == 'and':
                #end expression -> expression AND expression
                t = Node(x_and)
            elif p[2] == 'or':
                #end expression -> expression OR expression
                t = Node(x_or)
            elif p[2] == '<':
                #end expression -> expression LT expression
                t = Node(x_lt)
            elif p[2] == '<=':
                #end expression -> expression LE expression
                t = Node(x_le)
            elif p[2] == '>':
                #end expression -> expression GT expression
                t = Node(x_gt)
            elif p[2] == '>=':
                #end expression -> expression GE expression
                t = Node(x_ge)
            elif p[2] == '==':
                #end expression -> expression EQ expression
                t = Node(x_eq)
            else:
                #end expression -> expression NEQ expression
                t = Node(x_neq)
            t.value = p[2]
            p[0].attach(p[1],t,p[3])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
#end p_expression


def p_expression_uminus(p):
    "expression : MINUS simple_expression %prec UMINUS"
    if y_show_productions:
        print("expression -> MINUS simple_expression")
    p[0] = Node(x_expression)
    if y_build_ptree:
        # expression -> MINUS simple_expression
        t = Node(x_minus)
        t.value = p[1]
        p[0].attach(t,p[2])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_uminus

def p_expression_not(p):
    "expression : NOT simple_expression %prec UNOT"
    if y_show_productions:
        print("expression -> NOT simple_expression")
    p[0] = Node(x_expression)
    if y_build_ptree:
        # expression -> NOT simple_expression
        t = Node(x_not)
        t.value = p[1]
        p[0].attach(t,p[2])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_not


def p_expression_par(p):
    "simple_expression : LP expression RP "
    if y_show_productions:
        print("simple_expression -> LP expression RP")
    p[0] = Node(x_expression)
    if y_build_ptree:
        # simple_expression -> LP expression RP
        t = Node(x_par)
        p[0].attach(t,p[2])
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_par


def p_expression_int_literal(p):
    "simple_expression : INT_LIT"
    if y_show_productions:
        print("simple_expression -> INT_LIT")
    p[0] = Node(x_expression)
    if y_build_ptree:
        t = Node(x_int_lit)
        t.value = p[1]
        p[0].attach(t)
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_int_literal


def p_expression_float_literal(p):
    "simple_expression : FLOAT_LIT"
    if y_show_productions:
        print("simple_expression -> FLOAT_LIT")
    p[0] = Node(x_expression)
    if y_build_ptree:
        t = Node(x_float_lit)
        t.value = p[1]
        p[0].attach(t)
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_float_literal


def p_expression_bool_literal(p):
    """simple_expression : FALSE
                         | TRUE """
    if y_show_productions:
        if p[1] == 'false':
            print("simple_expression -> FALSE")
        else:
            print("simple_expression -> TRUE")
    p[0] = Node(x_expression)
    if y_build_ptree:
        t = Node(x_bool_lit)
        t.value = p[1]
        p[0].attach(t)
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_bool_literal

def p_expression_noref(p):
    '''simple_expression : NOREF'''
    if y_show_productions:
        print('simple_expression -> NOREF')
    p[0] = Node(x_expression)
    if y_build_ptree:
        t = Node(x_noref)
        t.value = 'noref'
        p[0].attach(t)
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_noref



def p_expression_char_literal(p):
    "simple_expression : CHAR_LIT"
    if y_show_productions:
        print("simple_expression -> CHAR_LIT")
    p[0] = Node(x_expression)
    if y_build_ptree:
        t = Node(x_char_lit)
        t.value = p[1]
        p[0].attach(t)
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_char_literal


def p_expression_str_literal(p):
    "simple_expression : STRING_LIT "
    if y_show_productions:
        print("simple_expression -> STRING_LIT")
    p[0] = Node(x_expression)
    if y_build_ptree:
        t = Node(x_string_lit)
        t.value = p[1]
        p[0].attach(t)
        p[0].pline = pline(p,1)
        p[0].ppos = ppos(p,1)
#end p_expression_str_literal


def p_expression_var(p):
    """simple_expression : var"""
    if y_show_productions:
        print("simple_expression -> var")
    p[0] = Node(x_expression)
    if y_build_ptree:
        p[0].attach(p[1])
        p[0].pline = p[1].pline
        p[0].ppos = p[1].ppos
#end p_expression_var


def p_expression_arr(p):
    """simple_expression : arr"""
    if y_show_productions:
        print("simple_expression -> arr")
    p[0] = Node(x_expression)
    if y_build_ptree:
        p[0].attach(p[1])
        p[0].pline = p[1].pline
        p[0].ppos = p[1].ppos
#end p_expression_arr


def p_expression_call(p):
    """simple_expression : call"""
    if y_show_productions:
        print("simple_expression -> call")
    p[0] = Node(x_expression)
    if y_build_ptree:
        p[0].attach(p[1])
        p[0].pline = p[1].pline
        p[0].ppos = p[1].ppos
#end p_expression_call

def p_arr(p):
    """ arr : ID_LS COLON RS
            | ID_LS COLON expression RS
            | ID_LS expression COLON RS
            | ID_LS expression COLON expression RS
            | qualifier ID_LS COLON RS
            | qualifier ID_LS COLON expression RS
            | qualifier ID_LS expression COLON RS
            | qualifier ID_LS expression COLON expression RS
            | ID_LS expression RS arr_tail
            | qualifier ID_LS expression RS arr_tail"""
    a = len(p)
    if y_show_productions:
        if p[2] == ':':
            if a == 4:
                print('arr -> ID_LS COLON RS')
            else:
                print('arr -> ID_LS COLON expression RS')
        elif p[3] == ':':
            if a == 5:
                if type(p[2]) == type('ab'):
                    print('arr -> qualifier ID_LS COLON RS')
                else:
                    print('arr -> ID_LS expression COLON RS')

            else:
                if type(p[2]) == type('ab'):
                    print('arr -> qualifier ID_LS COLON expression RS')
                else:
                    print('arr -> ID_LS expression COLON expression RS')
        else:
            if a >= 5:
                if p[4] == ':':
                    if a == 6:
                        print('arr -> qualifier ID_LS expression COLON RS')
                    else:
                        print('arr -> qualifier ID_LS expression COLON expression RS')
                else:
                    if a == 5:
                        print('arr -> ID_LS expression RS arr_tail')
                    else:
                        print('arr -> qualifier ID_LS expression RS arr_tail')
    p[0] = Node(x_arr)
    if y_build_ptree:
        if p[2] == ':':
            if a == 4:
                # arr -> ID_LS COLON RS
                p[0].nodeid = x_substr
                t = Node(x_id)
                t.value = p[1][:-1]
                r = Node(x_left)
                s = Node(x_right)
                p[0].attach(t,r,s)
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else:
                # arr -> ID_LS COLON expression RS
                p[0].nodeid = x_substr
                t = Node(x_id)
                t.value = p[1][:-1]
                r = Node(x_left)
                s = Node(x_right)
                s.attach(p[3])
                p[0].attach(t,r,s)
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
        elif p[3] == ':':
            if a == 5:
                if type(p[2]) == type('ab'):
                    # arr -> qualifier ID_LS COLON RS
                    p[0].nodeid = x_substr
                    t = Node(x_id)
                    t.value = p[1]+p[2][:-1]
                    r = Node(x_left)
                    s = Node(x_right)
                    p[0].attach(t,r,s)
                    p[0].pline = p[1].pline
                    p[0].ppos = p[1].ppos
                else:
                    # arr -> ID_LS expression COLON RS
                    p[0].nodeid = x_substr
                    t = Node(x_id)
                    t.value = p[1]
                    r = Node(x_left)
                    r.attach(p[2])
                    s = Node(x_right)
                    p[0].attach(t,r,s)
                    p[0].pline = pline(p,1)
                    p[0].ppos = ppos(p,1)
            else:
                if type(p[2]) == type('ab'):
                    # arr -> qualifier ID_LS COLON expression RS
                    p[0].nodeid = x_substr
                    t = Node(x_id)
                    t.value = p[1]+p[2][:-1]
                    r = Node(x_left)
                    s = Node(x_right)
                    s.attach(p[4])
                    p[0].attach(t,r,s)
                    p[0].pline = p[1].pline
                    p[0].ppos = p[1].ppos
                else:
                    # arr -> ID_LS expression COLON expression RS
                    p[0].nodeid = x_substr
                    t = Node(x_id)
                    t.value = p[1]
                    r = Node(x_left)
                    r.attach(p[2])
                    s = Node(x_right)
                    s.attach(p[4])
                    p[0].attach(t,r,s)
                    p[0].pline = pline(p,1)
                    p[0].ppos = ppos(p,1)
        else:
            if a >= 5:
                if p[4] == ':':
                    if a == 6:
                        # arr -> qualifier ID_LS expression COLON RS
                        p[0].nodeid = x_substr
                        t = Node(x_id)
                        t.value = p[1]+p[2][:-1]
                        r = Node(x_left)
                        r.attach(p[3])
                        s = Node(x_right)
                        p[0].attach(t,r,s)
                        p[0].pline = p[1].pline
                        p[0].ppos = p[1].ppos
                    else:
                        # arr -> qualifier ID_LS expression COLON expression RS
                        p[0].nodeid = x_substr
                        t = Node(x_id)
                        t.value = p[1]+p[2][:-1]
                        r = Node(x_left)
                        r.attach(p[3])
                        s = Node(x_right)
                        s.attach(p[5])
                        p[0].attach(t,r,s)
                        p[0].pline = p[1].pline
                        p[0].ppos = p[1].ppos
                else:
                    if a == 5:
                        # arr -> ID_LS expression RS arr_tail
                        t = Node(x_id)
                        t.value = p[1][:-1]
                        p[0].attach(t,p[2])
                        p[0].cond_attach(p[4])
                        p[0].pline = p[2].pline
                        p[0].ppos = p[2].ppos
                    else:
                        # arr -> qualifier ID_LS expression RS arr_tail
                        t = Node(x_id)
                        t.value = p[1]+p[2][:-1]
                        p[0].attach(t,p[3])
                        p[0].cond_attach(p[5])
                        p[0].pline = p[1].pline
                        p[0].ppos = p[1].ppos
#end p_arr


def p_arr_tail(p):
    """ arr_tail : LS expression RS arr_tail
                 | """
    a = len(p)
    if y_show_productions:
        if a == 5:
            print('arr_tail -> LS expression RS arr_tail')
        else:
            print('arr_tail -> epsilon')
    if y_build_ptree:
        if a == 5:
            # arr_tail -> LS expression RS arr_tail
            if len(p[4].children) == 0:
                p[0] = Node(x_arr)
                p[0].attach(p[2])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else:
                p[4].prettach(p[2])
                p[0] = p[4]
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
        else:
            # arr_tail -> epsilon
            p[0] = Node(x_arr)
#end p_arr_tail




def p_call(p):
    '''call : ID_LP par_list
            | BOOL_LP expression RP
            | CHAR_LP expression RP
            | STRING_LP expression RP
            | INT_LP expression RP
            | FLOAT_LP expression RP
            | FIN_DOT ID_LP par_list
            | FOUT_DOT ID_LP par_list
            | IDOF_LP expression RP
            | SIZEOF_LP size_par RP
            | TYPEOF_LP expression RP

            | qualifier ID_LP par_list'''
    a = len(p)
    if y_show_productions:
        if a == 3:
            print('call -> ID_LP par_list')
        else:
            if p[1] == 'bool(':
                print('call -> BOOL_LP expression RP')
            elif p[1] == 'char(':
                print('call -> CHAR_LP expression RP')
            elif p[1] == 'string(':
                print('call -> STRING_LP expression RP')
            elif p[1] == 'int(':
                print('call -> INT_LP expression RP')
            elif p[1] == 'float(':
                print('call -> FLOAT_LP expression RP')
            elif p[1] == 'fin.':
                print('call -> FIN_DOT ID_LP par_list')
            elif p[1] == 'fout.':
                print('call -> FOUT_DOT ID_LP par_list')
            elif p[1] == 'idof(':
                print('call -> IDOF_LP expression RP')
            elif p[1] == 'sizeof(':
                print('call -> SIZEOF_LP size_par RP')
            elif p[1] == 'typeof(':
                print('call -> TYPEOF_LP expression RP')
            else:
                print('call -> qualifier ID_LP par_list')
    p[0] = Node(x_call)
    if y_build_ptree:
        if a == 3:
            # call -> ID_LP par_list
            t = Node(x_id)
            t.value = p[1][:-1]
            p[0].attach(t)
            p[0].cond_attach(p[2])
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        else:
            if p[1] == 'bool(':
                # call -> BOOL_LP expression RP
                t = Node(x_id)
                t.value = p[1][:-1]
                p[0].attach(t,p[2])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1] == 'char(':
                # call -> CHAR_LP expression RP
                t = Node(x_id)
                t.value = p[1][:-1]
                p[0].attach(t,p[2])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1] == 'string(':
                # call -> STRING_LP expression RP
                t = Node(x_id)
                t.value = p[1][:-1]
                p[0].attach(t,p[2])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1] == 'int(':
                # call -> INT_LP expression RP
                t = Node(x_id)
                t.value = p[1][:-1]
                p[0].attach(t,p[2])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1] == 'float(':
                # call -> FLOAT_LP expression RP
                t = Node(x_id)
                t.value = p[1][:-1]
            elif p[1] == 'fin.':
                # call -> FIN_DOT ID_LP par_list
                t = Node(x_id)
                t.value = p[1]+p[2][:-1]
                p[0].attach(t)
                p[0].cond_attach(p[3])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1] == 'fout.':
                # call -> FOUT_DOT ID_LP par_list
                t = Node(x_id)
                t.value = p[1]+p[2][:-1]
                p[0].attach(t)
                p[0].cond_attach(p[3])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1] == 'idof(':
                # call -> IDOF_LP expression RP
                t = Node(x_id)
                t.value = p[1][:-1]
                t = Node(x_id)
                t.value = p[1][:-1]
                p[0].attach(t)
                p[0].cond_attach(p[2])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1] == 'sizeof(':
                # call -> SIZEOF_LP size_par RP
                t = Node(x_id)
                t.value = p[1][:-1]
                p[0].attach(t)
                p[0].cond_attach(p[2])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            elif p[1] == 'typeof(':
                # call -> TYPEOF_LP expression RP
                t = Node(x_id)
                t.value = p[1][:-1]
                p[0].attach(t)
                p[0].cond_attach(p[2])
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else:
                # call -> qualifier ID_LP par_list
                t = Node(x_id)
                t.value = p[1]+p[2][:-1]
                p[0].attach(t)
                p[0].cond_attach(p[3])
                p[0].pline = p[1].pline
                p[0].ppos = p[1].ppos
#end p_call


def p_size_par(p):
    '''size_par : ID
                | ID_LS type_tail
                | qualifier ID
                | qualifier ID_LS type_tail'''
    a = len(p)
    if y_show_productions:
        if a == 2:
            print('size_par -> ID')
        elif a == 3:
            if p[1][-1] == '[':
                print('size_par -> ID_LS type_tail')
            else:
                print('size_par -> qualifier ID')
        else:
            print('size_par -> qualifier ID_LS type_tail')
    p[0] = Node(x_par_list)
    if y_build_ptree:
        if a == 2:
            # size_par -> ID
            t = Node(x_id)
            t.value = p[1]
            p[0].attach(t)
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        elif a == 3:
            if p[1][-1] == '[':
                # size_par -> ID_LS type_tail
                t = Node(x_id)
                t.value = p[1][:-1]
                r = Node(x_dim)
                r.value = p[2]
                p[0].attach(t,r)
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else:
                # size_par -> qualifier ID
                t = Node(x_id)
                t.value = p[1]+p[2]
                p[0].attach(t)
                p[0].pline = p[1].pline
                p[0].ppos = p[1].ppos
        else:
            # size_par -> qualifier ID_LS type_tail
            t = Node(x_id)
            t.value = p[1]+p[2]
            r = Node(x_dim)
            t.value = p[3]
            p[0].attach(t,r)
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
#end p_size_par



def p_qualifier(p):
    """ qualifier : PARENT_DOT qualifier
                  | ID_DOT qualifier
                  | ID_DOT"""
    a = len(p)
    if y_show_productions:
        if a == 2:
            print("qualifier -> ID_DOT")
        else:
            if p[1][:-1] == 'parent':
                print('qualifier -> PARENT_DOT qualifier')
            else:
                print("qualifier -> ID_DOT qualifier")
        if y_build_ptree:
            if a == 2:
                # qualifier -> ID_DOT
                p[0] = Node(x_qualifier)
                p[0].value = p[1][:-1]
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
            else:
                # qualifier -> PARENT_DOT qualifier
                # qualifier -> ID_DOT qualifier
                p[0] = p[2]
                p[0].value = p[1]+p[2].value
                p[0].pline = pline(p,1)
                p[0].ppos = ppos(p,1)
#end p_qualifier


def p_var(p):
    """ var : ID
            | qualifier ID"""
    a = len(p)
    if y_show_productions:
        if a == 2:
            print("var -> ID")
        else:
            print("var -> qualifier ID")
    p[0] = Node(x_var)
    if y_build_ptree:
        if a == 2:
            p[0].value = p[1]
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
        else:
            p[0].value = p[1].value+p[2]
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
#end p_var

def p_par_list(p):
    """ par_list : RP
                 | expression RP
                 | expression COMMA par_list_tail """
    a = len(p)
    if y_show_productions:
        if a == 2:
            print("par_list -> RP")
        elif a == 3:
            print("par_list -> expression RP")
        else:
            print("par_list -> expression COMMA par_list_tail")
    p[0] = Node(x_par_list)
    if y_build_ptree:
        if a == 2:
            # par_list -> RP
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
            return
        elif a == 3:
            # par_list -> expression RP
            p[0].attach(p[1])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        else:
            # par_list -> expression COMMA par_list
            p[0].cond_attach(p[1],p[3])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
#end p_par_list


def p_par_list_tail(p):
    """ par_list_tail : RP
                      | expression RP
                      | expression COMMA par_list_tail """
    a = len(p)
    if y_show_productions:
        if a == 2:
            print("par_list_tail -> RP")
        elif a == 3:
            print("par_list_tail -> expression RP")
        else:
            print("par_list_tail -> expression COMMA par_list_tail")
    p[0] = Node(x_par_list_tail)
    if y_build_ptree:
        if a == 2:
            # par_list_tail -> RP
            p[0].pline = pline(p,1)
            p[0].ppos = ppos(p,1)
            return
        elif a == 3:
            # par_list_tail -> expression RP
            p[0].attach(p[1])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
        else:
            # par_list_tail -> expression COMMA par_list
            p[0].cond_attach(p[1],p[3])
            p[0].pline = p[1].pline
            p[0].ppos = p[1].ppos
#end p_par_list_tail


def p_error(t):
    if t:
        l = t.lineno
        p = t.lexpos - pangulex.y_last_newline
        print('[{},{}]'.format(l,p),"syntax error")
        print("offending line:")
        pangulex.show_line(l)
        sys.exit(0)
    else:
        print("syntax error at EOF")
        sys.exit(0)


def syn_error(message,p):
    print('[line {}]'.format(pline(p,1)),"error: ",message)
    print("offending line:\n {",end='')
    pangulex.show_line(pline(p,1))
    print("}")
    sys.exit(0)

def syn_warning(message,p):
    print("[line {}]".format(pline(p,1)),"warning: ",message)
    print("offending line:\n {",end='')
    pangulex.show_line(pline(p,1))
    print("}")
    return

def linepos(lineno,lexpos):
    global y_data
    # find start of line lineno
    if lineno == 1:
        start = 0
    else:
        lineno = lineno-1
        count = 0
        for i in range(len(y_data)):
            if y_data[i] == '\n':
                count += 1
                if count == lineno:
                    start = i
                    break
                #endif
            #endif
        #endfor
    return lexpos-start
#end linepos


def pline(p,i):
    return p.lineno(i)


def ppos(p,i):
    return linepos(p.lineno(i),p.lexpos(i))


def showp(p,n):
    y = Node(x_id)
    for i in range(n,len(p)):
        if type(p[i]) == type(y):
            print('p['+str(i)+']:',end='')
            p[i].show()
        else:
            print('p['+str(i)+']:',p[i])
#enddef


def is_name(xid):
    count = 0
    for i in xid:
        if i == '.':
            count = count+1
    return count == 0
#end is_name


# test lexer
def TestLexer(file):
    global y_data
    pangulex.y_show_tokens = True
    pangulex.y_show_comments = True
    f = open(file,"rt")
    if f.mode == "rt":
        y_data = f.read()
        f.close()
    else:
        print("can't open input file '"+file+"'")
        sys.exit(0)
    print(y_data)
    pangulex.lexer.input(y_data)
    while True:
        pangulex.lexer.token()
    #end while
#end TestLexar


def Parser(file):
    global y_show_symbol_table
    global y_build_symbol_table
    global y_show_productions
    global y_data
    global y_build_ptree
    global y_ptree
    global y_show_ptree
    global y_symbol_table
    global y_scope_stack
    y_ptree = None

    # set flags
    pangulex.y_show_tokens = False
    pangulex.y_show_comments = True
    y_show_productions = False
    y_build_ptree = True
    y_show_ptree = False
    y_deparse_ptree = False
    y_show_symbol_table = True
    y_build_symbol_table = True

    f = open(file,"rt")
    if f.mode == "rt":
        y_data = f.read()
        f.close()
    else:
        print("can't open input file '"+file+"'")
        sys.exit(0)
    print(y_data)
    #print("-------------------------------")
    pangupar = yacc.yacc()
    pangupar.parse(y_data,pangulex.lexer,False,False,None)
    print("parsing successful\n\n")
    if y_build_ptree:
        if y_show_ptree:
            print("parse tree:\n\n")
            y_ptree.showtree()
            print('-----------------------------')
        if y_deparse_ptree:
            print("deparse:\n\n")
            y_ptree.deparse()
            print('-----------------------------')
        if y_build_symbol_table:
            symbol_table = seman(y_ptree,None)
            if y_show_symbol_table:
                print("Semantic Module\n")
                symbol_table.showtab()
                check_var_def(y_ptree)
            #detect_error(y_ptree,symbol_table)



#end Parser


#TestLexer("xxx.asc")
Parser('xxx.asc')
