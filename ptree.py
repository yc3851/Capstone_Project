import sys
from xnames import *


def ex(x):
    print("***",x)
    sys.exit(0)

class Node:
    def __init__(self,nodeid,value=None):
        self.children = []
        self.nodeid = nodeid
        self.value = value
        self.pline = 0
        self.ppos = 0
        self.type = ''
        self.scope = ''
        self.type = ''
    #end __init__

    def leaf(self):
        return len(self.children) == 0

    def xid(self):
        print(ss(self),end='')

    def show(self):
        if self.leaf():
            self.xid()
            print(' -> ',end='')
            if type(self.value) == type("hello"):
                print('"'+self.value+'"')
            else:
                print(self.value)
        else:
            print(ss(self),"->",end='')
            for i in self.children:
                print(' ',ss(i)+" ",end='')
            print()
    #endshow

    def showe(self):
        self.show()
        sys.exit(0)
    #end showe

    def showtree(self):
        self.show()
        for i in self.children:
            if i.leaf():
                i.show()
            else:
                i.showtree()
    #end showtree


    # attach all nodes including leaves
    def attach(self,*argv):
        for arg in argv:
            if arg == None:
                continue
            else:
                self.children.append(arg)
    #end attach


    # attach only non-leaves
    def cond_attach(self,*argv):
        for arg in argv:
            if arg == None:
                continue
            elif len(arg.children) == 0:  # it is a leaf
                continue
            else:
                self.children.append(arg)
    #end cond_attach
        

    def prettach(self,*argv):
        children=[]
        for arg in argv:
            if arg != None:
                children.append(arg)
        self.children = children+self.children
    #end prettach


    def dd(self):
        for n in self.children:
            if type(n) == type(self):
                n.deparse()
            else:
                print('\nparent node ',end='')
                self.xid()
                print('\nchild node type',type(n))
                print('***[',n,']')
    #end dd

    def dd1(self,i):
        for n in range(i,len(self.children)):
            if type(self.children[n]) == type(self):
                self.children[n].deparse()
            else:
                print('\nparent ',end='')
                self.xid()
                print('\nchild of type',type(self.children[n]))
                print('***[',self.children[n],']')
    #end dd1


    def deparse(self) :

        a = len(self.children)

        ###############################################################
        #  x_compilation_unit -> [x_sections] [x_main_body]
        ###############################################################
        if self.nodeid == x_compilation_unit:
            if a == 0:
                print('main:\nendmain')
            elif a == 1:
                if self.children[0].nodeid == x_sections:
                    self.children[0].deparse()
                    print('main:\nendmain')
                else:
                    print('main:')
                    self.children[0].deparse()
                    print('endmain')
            else:
                self.children[0].deparse()
                print('main:')
                self.children[1].deparse()
                print('endmain')
            return
        
        if self.nodeid == x_main_section:
            #print('main : ')
            self.dd()
            #print('endmain')
            return

        ##############################################################
        # x_main_body -> [x_smt] [x_main_body]
        #             -> [x_var_definition] [x_main_body]
        ##############################################################
        if self.nodeid == x_main_body:
            self.dd()
            return

            
        ##############################################################
        #   x_sections -> x_var_definition  [x_sections]
        #              -> x_class_definition  [x_sections]
        ##############################################################
        if self.nodeid == x_sections:
            self.dd()
            return

    
        ##############################################################
        # x_var_definition  -> x_type  x_var_list
        #                   -> x_permanent x_type x_var_list
        #                   -> x_const x_type x_var_list
        #                   -> x_permanent_const x_type x_var_list
        ##############################################################
        if self.nodeid == x_var_definition:
            self.dd()
            print(';')
            return
            

        ##############################################################
        # x_class_definition -> x_class_header
        ##############################################################
        if self.nodeid == x_class_definition:
            self.dd()
            return


        ##############################################################
        # x_class_header -> x_id [x_class_body]
        #                -> x_id x_id [x_class_body]
        ##############################################################
        if self.nodeid == x_class_header:
            if a == 1:
                print('class',self.children[0].value+':\nendclass')
            elif a == 2:
                if self.children[1].nodeid == x_id:
                    print('class',self.children[0].value,'extends ',end='')
                    print(self.children[1].value+':\nendclass')
                else:
                    print('class',self.children[0].value+':')
                    self.children[1].deparse()
                    print('endclass')
            else:
                print('class',self.children[0].value,'extends ',end='')
                print(self.children[1].value+':')
                self.children[2].deparse()
                print('endclass')
            return
                    
             
        ##############################################################
        # x_var_list -> x_id [x_var_list_tail]
        #       -> x_id x_assig x_expression [x_var_list_tail]
        #       -> x_id x_passig x_expression [x_var_list_tail]
        #       -> x_id x_passig x_id [x_par_list_tail]
        #       -> x_id x_alloc x_id [x_par_list] [x_var_list_tail]
        ##############################################################
        if self.nodeid == x_var_list:
            if a == 1:
                self.children[0].deparse()
                return
            
            if self.children[1].nodeid == x_alloc:
                self.children[0].deparse()
                print('@=alloc ',end='')
                self.children[2].deparse()
                print('(',end='')
                if a == 3:
                    print(')',end='')
                elif a == 4:
                    if self.children[3].nodeid == x_par_list:
                        self.children[3].deparse()
                        print(')',end='')
                    else:
                        print(')',end='')
                        self.children[3].deparse()
                else:
                    self.children[3].deparse()
                    print(')',end='')
                    self.children[4].deparse()
            else:
                self.dd()
            return

        ##############################################################
        # x_var_list_tail -> x_id [x_var_list_tail]
        #       -> x_id x_assig x_expression [x_var_list_tail]
        #       -> x_id x_passig x_expression [x_var_list_tail]
        #       -> x_id x_passig x_id [x_par_list_tail]
        #       -> x_id x_alloc x_id [x_par_list] [x_var_list_tail]
        ##############################################################
        if self.nodeid == x_var_list_tail:
            print(',',end='')
            if a == 1:
                self.children[0].deparse()
                return
            
            if self.children[1].nodeid == x_alloc:
                self.children[0].deparse()
                print('@=alloc ',end='')
                self.children[2].deparse()
                print('(',end='')
                if a == 3:
                    print(')',end='')
                elif a == 4:
                    if self.children[3].nodeid == x_par_list:
                        self.children[3].deparse()
                        print(')',end='')
                    else:
                        print(')',end='')
                        self.children[3].deparse()
                else:
                    self.children[3].deparse()
                    print(')',end='')
                    self.children[4].deparse()
            else:
                self.dd()
            return

        ##############################################################
        # x_type -> x_bool [x_dim]
        #        -> x_char [x_dim]
        #        -> x_string [x_dim]
        #        -> x_int [x_dim]
        #        -> x_float [x_dim]
        #        -> x_id [x_dim]
        ##############################################################
        if self.nodeid == x_type:
            self.children[0].deparse()
            if a == 2:
                dim = self.children[1].value
                for i in range(dim):
                    print('[]',end='')
            print(' ',end='')
            return

        ##############################################################
        # x_atype -> x_bool [x_dim] [x_at]
        #         -> x_char [x_dim] [x_at]
        #         -> x_string [x_dim] [x_at]
        #         -> x_int [x_dim] [x_at]
        #         -> x_float [x_dim] [x_at]
        #         -> x_id [x_dim] [x_at]
        ##############################################################
        if self.nodeid == x_atype:
            self.children[0].deparse()
            if a == 2:
                if self.children[1].nodeid == x_dim:
                    dim = self.children[1].value
                    for i in range(dim):
                        print('[]',end='')
                else:
                    print('&',end='')
            else:
                dim = self.children[1].value
                for i in range(dim):
                    print('[]',end='')
                print('&',end='')
            print(' ',end='')
            return


        ##############################################################
        # x_stms -> x_stm [x_stms]
        ##############################################################
        if self.nodeid == x_stms:
            self.children[0].deparse()
            return

    
        ##############################################################
        # x_stm -> [x_id] x_null_stm
        #       -> [x_id] x_assig_stm
        #       -> [x_id] x_passig_stm
        #       -> [x_id] x_return_stm
        #       -> [x_id] x_preturn_stm
        #       -> [x_id] x_call_stm
        #       -> [x_id] x_if_stm
        #       -> [x_id] x_while_stm
        #       -> [x_id] x_for_stm
        #       -> [x_id] x_goto_stm
        #       -> [x_id] x_break_stm
        #       -> [x_id] x_continue_stm
        #       -> [x_id] x_guard_stm
        #       -> [x_id] x_raise_stm
        #       -> [x_id] x_terminate_stm
        ##############################################################
        if self.nodeid == x_stm:
            if self.children[0].nodeid == x_id:
                print(self.children[0].value+':',end='')
                self.children[1].deparse()
            else:
                self.children[0].deparse()
            return


        ##############################################################
        # x_class_body -> x_attr_definition [x_class_body]
        #       -> x_pulic x_method_definition [x_class_body]
        #       -> x_private x_method_definition [x_class_body]
        ##############################################################
        if self.nodeid == x_class_body:
            self.dd()
            return

        
        ##############################################################
        # x_attr_definition -> x_public_shared_const x_type x_var_list
        #                   -> x_private_shared_const x_type x_var_list
        #                   -> x_public_shared x_type x_var_list
        #                   -> x_private_shared x_type x_var_list
        #                   -> x_public_const x_type x_var_list
        #                   -> x_private_const x_type x_var_list
        #                   -> x_public x_type x_var_list
        #                   -> x_private x_type x_var_list
        ###############################################################
        if self.nodeid == x_attr_definition:
            self.dd()
            print(';')
            return


        ###############################################################
        # x_method_definition -> x_method_header [x_method_body]
        ###############################################################
        if self.nodeid == x_method_definition:
            self.dd()
            print('endmethod')
            return


        ###############################################################
        # x_method_header -> x_public x_id [x_arg_list] [x_type]
        #                 -> x_private x_id [x_arg_list] [x_type]
        ###############################################################
        if self.nodeid == x_method_header:
            self.children[0].deparse()
            print(' method ',end='')
            self.children[1].deparse()
            if a == 2:
                print('() :')
            elif a == 3:
                if self.children[2].nodeid == x_arg_list:
                    print('(',end='')
                    self.children[2].deparse()
                    print(') :')
                else:
                    print('() --> ',end='')
                    self.children[2].deparse()
                    print(' :')
            else:
                print('(',end='')
                self.children[2].deparse()
                print(') --> ',end='')
                self.children[3].deparse()
                print(' :')
            return


        ###############################################################
        # x_arg_list -> x_atype x_id [x_arg_list_tail]
        ###############################################################
        if self.nodeid == x_arg_list:
            self.dd()
            return


        ###############################################################
        # x_arg_list-tail -> x_atype x_id [x_arg_list_tail]
        ###############################################################
        if self.nodeid == x_arg_list_tail:
            print(',',end='')
            self.dd()
            return


        ###############################################################
        # x_method_body -> x_stm [x_method_body]
        #               -> x_var_definition [x_method_body]
        ###############################################################
        if self.nodeid == x_method_body:
            self.dd()
            return
            
        
        ###############################################################
        # x_break_stm ->
        ###############################################################
        if self.nodeid == x_break_stm:
            print('break;')
            return


        ###############################################################
        # x_continue_stm ->
        ###############################################################
        if self.nodeid == x_continue_stm:
            print('continue;')
            return


        ###############################################################
        # x_terminate_stm ->
        ###############################################################
        if self.nodeid == x_terminate_stm:
            print('terminate;')
            return


        ###############################################################
        # x_null_stm ->
        ###############################################################
        if self.nodeid == x_null_stm:
            print(';')
            return


        ###############################################################
        # x_assig_stm -> x_arr x_expression
        #             -> x_substr x_expression
        #             -> x_var x_expression
        ###############################################################
        if self.nodeid == x_assig_stm:
            self.children[0].deparse()
            print('=',end='')
            self.children[1].deparse()
            print(';')
            return


        ###############################################################
        # x_passig_stm -> x_arr x_expression
        #              -> x_substr x_expression
        #              -> x_var x_expression
        #              -> x_arr x_alloc x_id [x_par_list]
        #              -> x_substr x_alloc x_id [x_par_list]
        #              -> x_var x_alloc x_id [x_par_list]
        ###############################################################
        if self.nodeid == x_passig_stm:
            self.children[0].deparse()
            print('@=',end='')
            if self.children[1].nodeid == x_alloc:
                print(' alloc ',end='')
                self.children[2].deparse()
                print('(',end='')
                if a == 4:
                    self.children[3].deparse()
                print(');')
            else:
                self.children[1].deparse()
                print(';')
            return
            


        ###############################################################
        # x_call_stm -> x_call
        ###############################################################
        if self.nodeid == x_call_stm:
            self.children[0].deparse()
            print(';')
            return


        ###############################################################
        # x_if_stm -> [x_expression] [x_stms] [x_stms]
        ###############################################################
        if self.nodeid == x_if_stm:
            if a == 0:
                print('if then else endif')
            elif a == 1:
                if self.children[0].nodeid == x_expression:
                    print('if ',end='')
                    self.children[0].deparse()
                    print(' then  else endif')
                elif self.children[0].nodeid == x_stms:
                    print('if then ',end='')
                    self.children[0].deparse()
                    print('else endif')
            elif a == 2:
                if self.children[0].nodeid == x_expression:
                    print('if ',end='')
                    self.children[0].deparse()
                    print(' then')
                    self.children[1].deparse()
                    print(' else endif')
                elif self.children[0].nodeid == x_stms:
                    print('if then',end='')
                    self.children[0].deparse()
                    print('else',end='')
                    self.children[1].deparse()
                    print('endif')
            else:
                print('if ',end='')
                self.children[0].deparse()
                print(' then')
                self.children[1].deparse()
                print(' else')
                self.children[2].deparse()
                print('endif')
            return


        ###############################################################
        # x_while_stm -> [x_expression] [x_stms]
        ###############################################################
        if self.nodeid == x_while_stm:
            print('while ',end='')
            if a == 0:
                print('do endwhile')
            elif a == 1:
                if self.children[0].nodeid == x_expression:
                    self.children[0].deparse()
                    print(' do  endwhile')
                else:
                    print('do')
                    self.children[0].deparse()
                    print('endwhile')
            else:
                self.children[0].deparse()
                print(' do')
                self.children[1].deparse()
                print('endwhile')
            return


        ################################################################
        # x_for_stm -> [x_prologue] [x_condition] [x_epilogue] [x_stms]
        ################################################################
        if self.nodeid == x_for_stm:
            print('for ',end='')
            if a == 0:
                print('; ; do endfor')
            elif a == 1:
                if self.children[0].nodeid == x_prologue:
                    self.chdilren[0].deparse()
                    print('; ; do endfor')
                elif self.children[0].nodeid == x_condition:
                    print(' ;',end='')
                    self.children[0].deparse()
                    print('; do  endfor')
                elif self.children[0].nodeid == x_epilogue:
                    print("; ;",end='')
                    self.children[0].deparse()
                    print(' do  endfor')
                else:
                    print('; ; do')
                    self.children[0].deparse()
                    print('endfor')
            elif a == 2:
                if self.children[0].nodeid == x_prologue:
                    if self.children[1].nodeid == x_condition:
                        self.children[0].deparse()
                        print(';',end='')
                        self.children[1].deparse()
                        print('; do  endfor')
                    elif self.children[1].nodeid == x_epilogue:
                        self.children[0].deparse()
                        print('; ;',end='')
                        self.children[1].deparse()
                        print(" do enfor")
                    else:
                        self.children[0].deparse()
                        print('; ; do')
                        self.children[1].deparse()
                        print('endfor')
                elif self.children[0].nodeid == x_condition:
                    if self.children[1].nodeid == x_epilogue:
                        print(';',end='')
                        self.children[0].deparse()
                        print(';',end='')
                        self.children[1].deparse()
                        print(' do endofor')
                    else:
                        print(';',end='')
                        self.children[0].deparse()
                        print('; do')
                        self.children[1].deparse();
                        print('endfor')
                else:
                    print('; ;',end='')
                    self.children[0].deparse()
                    print(' do')
                    self.children[1].deparse()
                    print('endfor')
            elif a == 3:
                if self.children[0].nodeid == x_prologue:
                    if self.children[1].nodeid == x_condition:
                        if self.children[2].nodeid == x_epilogue:
                            self.children[0].deparse()
                            print(';',end='')
                            self.children[1].deparse()
                            print(';',end='')
                            self.children[2].deparse()
                            print('do endfor')
                        else:
                            self.children[0].deparse()
                            print(';',end='')
                            self.children[1].deparse()
                            print('; do')
                            self.children[2].deparse()
                            print('endfor')
                    else:
                        self.children[0].deparse()
                        print('; ;')
                        self.children[1].deparse()
                        print(' do')
                        self.children[2].deparse()
                        print('endfor')
                else:
                    print(' ;',end='')
                    self.children[0].deparse()
                    print(';',end='')
                    self.children[1].deparse()
                    print(' do')
                    self.children[2].deparse()
                    print('endfor')
            else:
                self.children[0].deparse()
                print(';',end='')
                self.children[1].deparse()
                print(';',end='')
                self.children[2].deparse()
                print(' do')
                self.children[3].deparse()
                print('endfor')
            return


        ################################################################
        # x_goto_stm ->
        ################################################################
        if self.nodeid == x_goto_stm:
            print('goto',self.value+';')
            return


        ################################################################
        # x_prologue -> x_arr x_assig x_expression [x_prologue_tail]
        #            -> x_substr x_assig x_expression [x_prologue_tail]
        #            -> x_var x_assig x_expression [x_prologue_tail]
        ################################################################
        if self.nodeid == x_prologue:
            self.dd()
            return


        ################################################################
        # x_prologue_tail -> x_arr x_assig x_expression [x_prologue_tail]
        #                 -> x_substr x_assig x_expression [x_prologue_tail]
        #                 -> x_var x_assig x_expression [x_prologue_tail]
        ################################################################
        if self.nodeid == x_prologue_tail:
            print(',',end='')
            self.dd()
            return
                

        ################################################################
        # x_condition -> x_expression
        ################################################################
        if self.nodeid == x_condition:
            self.children[0].deparse()
            return


        ################################################################
        # x_epilogue -> x_arr x_assig x_expression [x_epilogue_tail]
        #            -> x_substr x_assig x_expression [x_epilogue_tail]
        #            -> x_var x_assig x_expression [x_epilogue_tail]
        ################################################################
        if self.nodeid == x_epilogue:
            self.dd()
            return


        ################################################################
        # x_epilogue_tail -> x_arr x_assig x_expression [x_epilogue_tail]
        #                 -> x_substr x_assig x_expression [x_epilogue_tail]
        #                 -> x_var x_assig x_expression [x_epilogue_tail]
        ################################################################
        if self.nodeid == x_epilogue_tail:
            print(',',end='')
            self.dd()
            return


        ################################################################
        # x_return_stm -> [x_expression]
        ################################################################
        if self.nodeid == x_return_stm:
            if a == 0:
                print('return;')
            else:
                print('return ',end='')
                self.children[0].deparse()
                print(';')
            return


        ################################################################
        # x_preturn_stm -> [x_expression]
        ################################################################
        if self.nodeid == x_preturn_stm:
            if a == 0:
                print('@return ????')
            else:
                print("@return ",end='')
                self.children[0].deparse()
                print(';')
            return



        ################################################################
        # x_guard_stm -> [x_stms] [x_catch_block]
        ################################################################
        if self.nodeid == x_guard_stm:
            if a == 0:
                print('guard:  catch endcatch')
            elif a == 1:
                if self.children[0].nodeid == x_stms:
                    print('guard:')
                    self.children[0].deparse()
                    print('catch:  endcatch')
                else:
                    print('guard:  catch:')
                    self.children[0].deparse()
                    print('endcatch')
            else:
                print('guard:')
                self.children[0].deparse()
                print('catch:')
                self.children[1].deparse()
                print('endcatch')
            return


        ################################################################
        # x_catch_block -> x_catch_label [x_stms] [x_catch_block_tail]
        ################################################################
        if self.nodeid == x_catch_block:
            print('"'+self.children[0].value+'":')
            self.dd1(1)
            return


        ################################################################
        # x_catch_block_tail -> x_catch_label [x_stms] [x_catch_block_tail]
        ################################################################
        if self.nodeid == x_catch_block_tail:
            print('"'+self.children[0].value+'":')
            self.dd1(1)
            return
            

        ################################################################
        # x_raise_stm -> x_expression
        ################################################################
        if self.nodeid == x_raise_stm:
            print('raise ',end='')
            self.children[0].deparse()
            print(';')
            return
        

        ################################################################
        # x_expression -> x_expression x_plus x_expression
        #              -> x_expression x_minus x_expression
        #              -> x_expression x_mul x_expression
        #              -> x_expression x_div x_expression
        #              -> x_expression x_idiv x_expression
        #              -> x_expression x_mod x_expression
        #              -> x_expression x_and x_expression
        #              -> x_expression x_or x_expression
        #              -> x_expression x_lt x_expression
        #              -> x_expression x_le x_expression
        #              -> x_expression x_gt x_expression
        #              -> x_expression x_ge x_expression
        #              -> x_expression x_eq x_expression
        #              -> x_expression x_neq x_expression
        #              -> x_minus x_expression
        #              -> x_not x_expression
        #              -> x_par x_expression
        #              -> x_int_lit
        #              -> x_float_lit
        #              -> x_bool_lit
        #              -> x_noref
        #              -> x_char_lit
        #              -> x_string_lit
        #              -> x_var
        #              -> x_arr
        #              -> x_substr
        #              -> x_call
        ################################################################
        if self.nodeid == x_expression:
            if self.children[0].nodeid == x_par:
                print('(',end='')
                self.children[1].deparse()
                print(')',end='')
            else:
                self.dd()
            return


        ################################################################
        # x_substr -> x_id [x_left] [x_right]
        ################################################################
        if self.nodeid == x_substr:
            self.children[0].deparse()
            if a == 1:
                print('[ : ]')
            elif a == 2:
                if self.children[1].noidei == x_left:
                    print('[',end='')
                    self.children[1].deparse()
                    print(': ]',end='')
                else:
                    print('[ :',end='')
                    self.children[1].deparse()
                    print(']',end='')
            else:
                print('[',end='')
                self.children[1].deparse()
                print(':',end='')
                self.children[2].deparse()
                print(']',end='')
            return
                


        ################################################################
        # x_arr -> x_id [x_expression]*
        ################################################################
        if self.nodeid == x_arr:
            first = True
            for i in self.children:
                if first:
                    i.deparse()
                    first = False
                else:
                    print('[',end='')
                    i.deparse()
                    print(']',end='')
            return


        ###############################################################
        # x_call -> x_id [x_par_list]
        ###############################################################
        if self.nodeid == x_call:
            self.children[0].deparse()
            print('(',end='')
            if a == 2:
                self.children[1].deparse()
            print(')',end='')
            return
            

        ###############################################################
        # x_var ->
        ###############################################################
        if self.nodeid == x_var:
            print(self.value,end='')
            return

        ################################################################
        # x_par_list -> x_expression [x_par_list_tail]
        #            -> x_id x_dim
        ################################################################
        if self.nodeid == x_par_list:
            if a == 1:
                self.children[0].deparse()
            else:
                if self.children[0].nodeid == x_id:
                    self.children[0].deparse()
                    for i in range(self.children[1].vaue):
                        print('[]',end='')
                else:
                    self.dd()
            return
            

        ################################################################
        # x_par_list_tail -> x_expression [x_par_list_tail]
        ################################################################
        if self.nodeid == x_par_list_tail:
            print(',',end='')
            if a == 1:
                self.children[0].deparse()
            else:
                if self.children[0].nodeid == x_id:
                    self.children[0].deparse()
                    for i in range(self.children[1].vaue):
                        print('[]',end='')
                else:
                    self.dd()
            return

        ###############################################################
        # x_id
        ###############################################################
        if self.nodeid == x_id:
            print(self.value,end='')
            return

        ###############################################################
        # x_bool
        ###############################################################
        if self.nodeid == x_bool:
            print('bool',end='')
            return

        ###############################################################
        # x_char
        ###############################################################
        if self.nodeid == x_char:
            print('char',end='')
            return

        ###############################################################
        # x_string
        ###############################################################
        if self.nodeid == x_string:
            print('string',end='')
            return

        ###############################################################
        # x_int
        ###############################################################
        if self.nodeid == x_int:
            print('int',end='')
            return

        ###############################################################
        # x_float
        ###############################################################
        if self.nodeid == x_float:
            print('float',end='')
            return


        ###############################################################
        # x_assig
        ###############################################################
        if self.nodeid == x_assig:
            print('=',end='')
            return

        ###############################################################
        # x_passig
        ###############################################################
        if self.nodeid == x_passig:
            print('@=',end='')
            return

        ###############################################################
        # x_lt
        ###############################################################
        if self.nodeid == x_lt:
            print('<',end='')
            return

        ###############################################################
        # x_le
        ###############################################################
        if self.nodeid == x_le:
            print('<=',end='')
            return

        ###############################################################
        # x_gt
        ###############################################################
        if self.nodeid == x_gt:
            print('>',end='')
            return

        ###############################################################
        # x_ge
        ###############################################################
        if self.nodeid == x_ge:
            print('>=',end='')
            return

        ###############################################################
        # x_eq
        ###############################################################
        if self.nodeid == x_eq:
            print('==',end='')
            return

        ###############################################################
        # x_neq
        ###############################################################
        if self.nodeid == x_neq:
            print('!=',end='')
            return

        ###############################################################
        # x_plus
        ###############################################################
        if self.nodeid == x_plus:
            print('+',end='')
            return

        ###############################################################
        # x_minus
        ###############################################################
        if self.nodeid == x_minus:
            print('-',end='')
            return

        ###############################################################
        # x_mul
        ###############################################################
        if self.nodeid == x_star:
            print('*',end='')
            return

        ###############################################################
        # x_div
        ###############################################################
        if self.nodeid == x_div:
            print('/',end='')
            return

        ###############################################################
        # x_idiv
        ###############################################################
        if self.nodeid == x_idiv:
            print('//',end='')
            return

        ###############################################################
        # x_mod
        ###############################################################
        if self.nodeid == x_mod:
            print(' mod ',end='')
            return

        ###############################################################
        # x_and
        ###############################################################
        if self.nodeid == x_and:
            print(' and ',end='')
            return

        ###############################################################
        # x_or
        ###############################################################
        if self.nodeid == x_or:
            print(' or ',end='')
            return

        ###############################################################
        # x_not
        ###############################################################
        if self.nodeid == x_not:
            print(' not ',end='')
            return


        ###############################################################
        # x_alloc
        ###############################################################
        if self.nodeid == x_alloc:
            print(' alloc ',end='')
            return

        ###############################################################
        # x_bool_lit
        ###############################################################
        if self.nodeid == x_bool_lit:
            print(self.value,end='')
            return
        
        ###############################################################
        # x_char_lit
        ###############################################################
        if self.nodeid == x_char_lit:
            print("'"+self.value+"'",end='')
            return

        ###############################################################
        # x_string_lit
        ###############################################################
        if self.nodeid == x_string_lit:
            print('"'+self.value+'"',end='')
            return

        ###############################################################
        # x_int_lit
        ###############################################################
        if self.nodeid == x_int_lit:
            print(self.value,end='')
            return

        ###############################################################
        # x_float_lit
        ###############################################################
        if self.nodeid == x_float_lit:
            print(self.value,end='')
            return

        ###############################################################
        # x_permanent
        ###############################################################
        if self.nodeid == x_permanent:
            print('permanent ',end='')
            return

        ###############################################################
        # x_const
        ###############################################################
        if self.nodeid == x_const:
            print('const ',end='')
            return

        ###############################################################
        # x_shared
        ###############################################################
        if self.nodeid == x_shared:
            print('shared ',end='')
            return

        ###############################################################
        # x_public
        ###############################################################
        if self.nodeid == x_public:
            print('public ',end='')
            return

        ###############################################################
        # x_private
        ###############################################################
        if self.nodeid == x_private:
            print('private ',end='')
            return

        ###############################################################
        # x_permanent_const
        ###############################################################
        if self.nodeid == x_permanent_const:
            print('permanent const ',end='')
            return

        ###############################################################
        # x_public_shared
        ###############################################################
        if self.nodeid == x_public_shared:
            print('public shared ',end='')
            return

        ###############################################################
        # x_public_const
        ###############################################################
        if self.nodeid == x_public_const:
            print('public const ',end='')
            return

        ###############################################################
        # x_private_const
        ###############################################################
        if self.nodeid == x_private_const:
            print('private const ',end='')
            return

        ###############################################################
        # x_private_shared
        ###############################################################
        if self.nodeid == x_private_shared:
            print('private shared ',end='')
            return

        ###############################################################
        # x_public_shared_const
        ###############################################################
        if self.nodeid == x_public_shared_const:
            print('public shared const ',end='')
            return


        ###############################################################
        # x_private_shared_const
        ###############################################################
        if self.nodeid == x_private_shared_const:
            print('private shared const ',end='')
            return

        ###############################################################
        # x_noref
        ###############################################################
        if self.nodeid == x_noref:
            print('noref',end='')
            return

        print("*** unexpected nodeid",ss(self))
        sys.exit()
#end deparse()


        
#end class Node


    
