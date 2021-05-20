# define values of x_names
x_alloc                    =1
x_and                      =2
x_arg_list                 =3
x_arg_list_tail            =4
x_arr                      =5
x_assig                    =6
x_assig_stm                =7
x_at                       =8
x_attr_definition          =9
x_atype                    =10
x_bool                     =11
x_bool_lit                 =12
x_break_stm                =13
x_call                     =14
x_call_stm                 =15
x_catch_block              =16
x_catch_block_tail         =17
x_catch_label              =18
x_char                     =19
x_char_lit                 =20
x_class_body               =21
x_class_definition         =22
x_class_header             =23
x_comma                    =24
x_compilation_unit         =25
x_condition                =26
x_const                    =27
x_continue_stm             =28
x_dim                      =29
x_dimlist                  =30
x_div                      =31
x_epilogue                 =32
x_epilogue_tail            =33
x_eq                       =34
x_expression               =35
x_false                    =36
x_file                     =37
x_float                    =38
x_float_lit                =39
x_for_stm                  =40
x_ge                       =41
x_goto_stm                 =42
x_gt                       =43
x_guard_stm                =44
x_id                       =45
x_id_dot                   =46
x_idiv                     =47
x_if_stm                   =48
x_int                      =49
x_int_lit                  =50
x_le                       =51
x_left                     =52
x_lrs                      =53
x_lt                       =54
x_main_body                =55
x_main_section             =56
x_method_body              =57
x_method_definition        =58
x_method_header            =59
x_minus                    =60
x_mod                      =61
x_neq                      =62
x_noref                    =63
x_not                      =64
x_null_stm                 =65
x_or                       =66
x_par                      =67
x_par_expression           =68
x_par_list                 =69
x_par_list_tail            =70
x_passig                   =71
x_passig_stm               =72
x_permanent                =73
x_permanent_const          =74
x_plus                     =75
x_prefix                   =76
x_preturn_stm              =77
x_private                  =78
x_private_const            =79
x_private_shared           =80
x_private_shared_const     =81
x_prologue                 =82
x_prologue_tail            =83
x_public                   =84
x_public_const             =85
x_public_shared            =86
x_public_shared_const      =87
x_qualifier                =88
x_raise_stm                =89
x_return_stm               =90
x_right                    =91
x_rp                       =92
x_section                  =93
x_sections                 =94
x_shared                   =95
x_shared_const             =96
x_star                     =97
x_stm                      =98
x_stms                     =99
x_str_lit                  =100
x_string                   =101
x_string_lit               =102
x_substr                   =103
x_terminate_stm            =104
x_true                     =105
x_type                     =106
x_type_at                  =107
x_var                      =108
x_var_definition           =109
x_var_list                 =110
x_var_list_tail            =111
x_while_stm                =112

def ss(i):
    if i.nodeid == x_alloc:
        return 'x_alloc'
    elif i.nodeid == x_and:
        return 'x_and'
    elif i.nodeid == x_arg_list:
        return 'x_arg_list'
    elif i.nodeid == x_arg_list_tail:
        return 'x_arg_list_tail'
    elif i.nodeid == x_arr:
        return 'x_arr'
    elif i.nodeid == x_assig:
        return 'x_assig'
    elif i.nodeid == x_assig_stm:
        return 'x_assig_stm'
    elif i.nodeid == x_at:
        return 'x_at'
    elif i.nodeid == x_attr_definition:
        return 'x_attr_definition'
    elif i.nodeid == x_atype:
        return 'x_atype'
    elif i.nodeid == x_bool:
        return 'x_bool'
    elif i.nodeid == x_bool_lit:
        return 'x_bool_lit'
    elif i.nodeid == x_break_stm:
        return 'x_break_stm'
    elif i.nodeid == x_call:
        return 'x_call'
    elif i.nodeid == x_call_stm:
        return 'x_call_stm'
    elif i.nodeid == x_catch_block:
        return 'x_catch_block'
    elif i.nodeid == x_catch_block_tail:
        return 'x_catch_block_tail'
    elif i.nodeid == x_catch_label:
        return 'x_catch_label'
    elif i.nodeid == x_char:
        return 'x_char'
    elif i.nodeid == x_char_lit:
        return 'x_char_lit'
    elif i.nodeid == x_class_body:
        return 'x_class_body'
    elif i.nodeid == x_class_definition:
        return 'x_class_definition'
    elif i.nodeid == x_class_header:
        return 'x_class_header'
    elif i.nodeid == x_comma:
        return 'x_comma'
    elif i.nodeid == x_compilation_unit:
        return 'x_compilation_unit'
    elif i.nodeid == x_condition:
        return 'x_condition'
    elif i.nodeid == x_const:
        return 'x_const'
    elif i.nodeid == x_continue_stm:
        return 'x_continue_stm'
    elif i.nodeid == x_dim:
        return 'x_dim'
    elif i.nodeid == x_dimlist:
        return 'x_dimlist'
    elif i.nodeid == x_div:
        return 'x_div'
    elif i.nodeid == x_epilogue:
        return 'x_epilogue'
    elif i.nodeid == x_epilogue_tail:
        return 'x_epilogue_tail'
    elif i.nodeid == x_eq:
        return 'x_eq'
    elif i.nodeid == x_expression:
        return 'x_expression'
    elif i.nodeid == x_false:
        return 'x_false'
    elif i.nodeid == x_file:
        return 'x_file'
    elif i.nodeid == x_float:
        return 'x_float'
    elif i.nodeid == x_float_lit:
        return 'x_float_lit'
    elif i.nodeid == x_for_stm:
        return 'x_for_stm'
    elif i.nodeid == x_ge:
        return 'x_ge'
    elif i.nodeid == x_goto_stm:
        return 'x_goto_stm'
    elif i.nodeid == x_gt:
        return 'x_gt'
    elif i.nodeid == x_guard_stm:
        return 'x_guard_stm'
    elif i.nodeid == x_id:
        return 'x_id'
    elif i.nodeid == x_id_dot:
        return 'x_id_dot'
    elif i.nodeid == x_idiv:
        return 'x_idiv'
    elif i.nodeid == x_if_stm:
        return 'x_if_stm'
    elif i.nodeid == x_int:
        return 'x_int'
    elif i.nodeid == x_int_lit:
        return 'x_int_lit'
    elif i.nodeid == x_le:
        return 'x_le'
    elif i.nodeid == x_left:
        return 'x_lef'
    elif i.nodeid == x_lrs:
        return 'x_lrs'
    elif i.nodeid == x_lt:
        return 'x_lt'
    elif i.nodeid == x_main_body:
        return 'x_main_body'
    elif i.nodeid == x_main_section:
        return 'x_main_section'
    elif i.nodeid == x_method_body:
        return 'x_method_body'
    elif i.nodeid == x_method_definition:
        return 'x_method_definition'
    elif i.nodeid == x_method_header:
        return 'x_method_header'
    elif i.nodeid == x_minus:
        return 'x_minus'
    elif i.nodeid == x_mod:
        return 'x_mod'
    elif i.nodeid == x_neq:
        return 'x_neq'
    elif i.nodeid == x_noref:
        return 'x_noref'
    elif i.nodeid == x_not:
        return 'x_not'
    elif i.nodeid == x_null_stm:
        return 'x_null_stm'
    elif i.nodeid == x_or:
        return 'x_or'
    elif i.nodeid == x_par:
        return 'x_par'
    elif i.nodeid == x_par_expression:
        return 'x_par_expression'
    elif i.nodeid == x_par_list:
        return 'x_par_list'
    elif i.nodeid == x_par_list_tail:
        return 'x_par_list_tail'
    elif i.nodeid == x_passig:
        return 'x_passig'
    elif i.nodeid == x_passig_stm:
        return 'x_passig_stm'
    elif i.nodeid == x_permanent:
        return 'x_permanent'
    elif i.nodeid == x_permanent_const:
        return 'x_permanent_const'
    elif i.nodeid == x_plus:
        return 'x_plus'
    elif i.nodeid == x_prefix:
        return 'x_prefix'
    elif i.nodeid == x_preturn_stm:
        return 'x_preturn_stm'
    elif i.nodeid == x_private:
        return 'x_private'
    elif i.nodeid == x_private_const:
        return 'x_private_const'
    elif i.nodeid == x_private_shared:
        return 'x_private_shared'
    elif i.nodeid == x_private_shared_const:
        return 'x_private_shared_const'
    elif i.nodeid == x_prologue:
        return 'x_prologue'
    elif i.nodeid == x_prologue_tail:
        return 'x_prologue_tail'
    elif i.nodeid == x_public:
        return 'x_public'
    elif i.nodeid == x_public_const:
        return 'x_public_const'
    elif i.nodeid == x_public_shared:
        return 'x_public_shared'
    elif i.nodeid == x_public_shared_const:
        return 'x_public_shared_const'
    elif i.nodeid == x_qualifier:
        return 'x_qualifier'
    elif i.nodeid == x_raise_stm:
        return 'x_raise_stm'
    elif i.nodeid == x_return_stm:
        return 'x_return_stm'
    elif i.nodeid == x_right:
        return 'x_right'
    elif i.nodeid == x_rp:
        return 'x_rp'
    elif i.nodeid == x_section:
        return 'x_section'
    elif i.nodeid == x_sections:
        return 'x_sections'
    elif i.nodeid == x_shared:
        return 'x_shared'
    elif i.nodeid == x_shared_const:
        return 'x_shared_const'
    elif i.nodeid == x_star:
        return 'x_star'
    elif i.nodeid == x_stm:
        return 'x_stm'
    elif i.nodeid == x_stms:
        return 'x_stms'
    elif i.nodeid == x_str_lit:
        return 'x_str_lit'
    elif i.nodeid == x_string:
        return 'x_string'
    elif i.nodeid == x_string_lit:
        return 'x_string_lit'
    elif i.nodeid == x_substr:
        return 'x_substr'
    elif i.nodeid == x_terminate_stm:
        return 'x_terminate_stm'
    elif i.nodeid == x_true:
        return 'x_true'
    elif i.nodeid == x_type:
        return 'x_type'
    elif i.nodeid == x_type_at:
        return 'x_type_at'
    elif i.nodeid == x_var:
        return 'x_var'
    elif i.nodeid == x_var_definition:
        return 'x_var_definition'
    elif i.nodeid == x_var_list:
        return 'x_var_list'
    elif i.nodeid == x_var_list_tail:
        return 'x_var_list_tail'
    elif i.nodeid == x_while_stm:
        return 'x_while_stm'
    else:
        return '????({})'.format(i.nodeid)
#end ss
