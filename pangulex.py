import ply.lex as lex
import sys

y_show_tokens = False
y_show_comments = False

reserved = {'alloc' : 'ALLOC',
            'and' :'AND',
            'bool' : 'BOOL',
            'break' : 'BREAK',
            'catch' : 'CATCH',
            'char' : 'CHAR',
            'class' : 'CLASS',
            'const' : 'CONST',
            'continue' : 'CONTINUE',
            'do' : 'DO',
            'else' : 'ELSE',
            'endcatch' : 'ENDCATCH',
            'endclass' : 'ENDCLASS',
            'endfor' : 'ENDFOR',
            'endif' : 'ENDIF',
            'endmain' : 'ENDMAIN',
            'endmethod' : 'ENDMETHOD',
            'endwhile' : 'ENDWHILE',
            'extends' : 'EXTENDS',
            'false' : 'FALSE',
            'File' : 'FILE',
            'float' : 'FLOAT',
            'for' : 'FOR',
            'goto' : 'GOTO',
            'guard' : 'GUARD',
            'if' : 'IF',
            'int' : 'INT',
            'main' : 'MAIN',
            'method' : 'METHOD',
            'mod' : 'MOD',
            'noref' : 'NOREF',
            'not' : 'NOT',
            'or' : 'OR',
            'permanent' : 'PERMANENT',
            'private' : 'PRIVATE',
            'public' : 'PUBLIC',
            'raise' : 'RAISE',
            'return' : 'RETURN',
            '@return' : 'PRETURN',
            'shared' : 'SHARED',
            'string' : 'STRING',
            'terminate' : 'TERMINATE',
            'then' : 'THEN',
            'true' : 'TRUE',
            'while' : 'WHILE'
}

protected = ['fin', 'fout', 'sizeof', 'typeof', 'idof']

def is_protected(id):
   for i in protected:
      if i == id:
         return True
   return False
#end is_protected


def digit(a):
   if len(a) == 1 and a <= '9' and a >= '0':
      return True
   else:
      return False
#end digit  


def is_reserved(id):
   global reserved
   for i in reserved:
      if i == id:
         return True
   return False
#end is_reserved


tokens = ['ARROW', 'ASSIG', 'BOOL_AT', 'BOOL_LP', 'BOOL_LS',
          'CHAR_AT', 'CHAR_LIT', 'CHAR_LP', 'CHAR_LS', 'COLON', 'COMMA',
          'DIV', 'EQ', 'FIN_DOT', 'FLOAT_AT', 'FLOAT_LIT',
          'FLOAT_LP', 'FLOAT_LS', 'FOUT_DOT', 'GE', 'GT', 'ID', 'IDIV',
          'ID_COLON', 'ID_AT', 'ID_DOT', 'ID_LP', 'ID_LS',
          'IDOF_LP', 'INT_AT', 'INT_LP', 'INT_LIT', 'INT_LS', 'LE', 'LP',
          'LS', 'LT', 'MINUS', 'NEQ', 'PARENT_DOT', 'PASSIG', 'PLUS', 'RLS',
          'RP', 'RS', 'RS_AT', 'SEMI', 'SIZEOF_LP', 'STAR', 'STRING_AT',
          'STRING_LIT', 'STRING_LP', 'STRING_LS',
          'TYPEOF_LP' ]+list(reserved.values())

t_ignore = " \t"

y_last_newline = 0

# Tokens

#     (# .... #)
def t_MULTILINE_COMMENT(t):
   r'\(\#(.|\n)*?\#\)'
   global y_last_newline
   ln = len(t.value)
   beg = lexer.lexpos-ln  # begenning of the comment
   for i in range(ln):
      if t.value[i] == '\n':
         t.lexer.lineno += 1
         y_last_newline = i
   if y_show_comments:
      print("*** multiline comment ************************************")
      print(t.value)
      print("**********************************************************")


def t_LINE_COMMENT(t):
   r'\#(.)*\n'
   global y_last_newline
   t.lexer.lineno += 1
   y_last_newline = lexer.lexpos-1
   if y_show_comments:
      print("*** comment **********************************************")
      print(t.value)
      print("**********************************************************")


def t_ARROW(t):
   r'-->'
   if y_show_tokens:
      print("   ",t)
   return t

def t_EQ(t):
   r'=='
   if y_show_tokens:
      print("   ",t)
   return t

def t_NEQ(t):
   r'!='
   if y_show_tokens:
      print("   ",t)
   return t


def t_GE(t):
   r'>='
   if y_show_tokens:
      print("   ",t)
   return  t

def t_GT(t):
   r'>'
   if y_show_tokens:
      print("   ",t)
   return  t


def t_LE(t):
   r'<='
   if y_show_tokens:
      print("   ",t)
   return  t

def t_LS(t):
   r'\['
   if y_show_tokens:
      print("   ",t)
   return  t

def t_LT(t):
   r'<'
   if y_show_tokens:
      print("   ",t)
   return  t

def t_COLON(t):
   r':'
   if y_show_tokens:
      print("   ",t)
   return t

def t_SEMI(t):
   r';'
   if y_show_tokens:
      print("   ",t)
   return t

def t_RLS(t):
   r'\]\['
   if y_show_tokens:
      print("   ",t)
   return t

def t_RS_AT(t):
   r'\][ ]*&'
   if y_show_tokens:
      print("   ",t)
   return t

def t_RS(t):
   r'\]'
   if y_show_tokens:
      print("   ",t)
   return t

def t_RP(t):
   r'\)'
   if y_show_tokens:
      print("   ",t)
   return t

def t_LP(t):
   r'\('
   if y_show_tokens:
      print("   ",t)
   return t

def t_IDIV(t):
   r'//'
   if y_show_tokens:
      print("   ",t)
   return t

def t_DIV(t):
   r'/'
   if y_show_tokens:
      print("   ",t)
   return t

def t_STAR(t):
   r'\*'
   if y_show_tokens:
      print("   ",t)
   return t

def t_PLUS(t):
   r'\+'
   if y_show_tokens:
      print("   ",t)
   return t

def t_MINUS(t):
   r'-'
   if y_show_tokens:
      print("   ",t)
   return t

def t_ASSIG(t):
   r'='
   if y_show_tokens:
      print("   ",t)
   return t

def t_PASSIG(t):
   r'@='
   if y_show_tokens:
      print("   ",t)
   return t

def t_COMMA(t):
   r","
   if y_show_tokens:
      print("   ",t)
   return t


def t_STRING_LIT(t):
   r'\"([^\\\"]|\\\\|\\\"|\\n|\\/|\\\d+)*\"'
   global y_last_newline
   lexem = t.value
   t.value = t.value[1:-1]
   i = 0
   a = len(t.value)
   while i < a:
      if t.value[i] == '\\':
         if i+1 < a:
            if t.value[i+1] == '\\':                  # case \\
               i += 2
               continue
            elif t.value[i+1] == '"':                 # case \"
               i += 2
               continue
            elif t.value[i+1] == 'n':                 # case \n
               i += 2
               continue
            elif t.value[i+1] == '/':                 # case \/
               i += 2
               continue
            if digit(t.value[i+1]):                   # case \d
               if i+2 < a:
                  if digit(t.value[i+2]):             # case \dd
                     if i+3 < a:
                        if digit(t.value[i+3]):       # case \ddd
                           i += 4
                           continue
                        elif t.value[i+3] == '/':     # case \dd/
                           i += 4
                           continue
                        elif t.value[i+3] == '\\':    # case \dd\
                           i += 3
                           continue
                        else:                         # case \ddA
                           i += 4
                           continue
                     else:                            # case \dd$
                        i += 3
                        continue
                  elif t.value[i+2] == '/':           # case \d/
                     i += 3
                     continue
                  elif t.value[i+2] == '\\':          # case \d\
                     i += 2
                     continue
                  else:                               # case \dA
                     i += 3
                     continue
               else:                                  # case \d$
                  i += 2
                  continue
            else:                                     # case \A
               lex_error("incorrect escaped sequence in string\n"+lexem,t)
         else:                                        # case \$
            lex_error("incorrect escaped sequence in string\n"+lexem,t)
      else:                                           # case A
         i += 1
         continue
   #end while
   if y_show_tokens:
      print("   ",t)
   return t
#end t_STRING_LIT


def t_CHAR_LIT(t):
   r"'[^.]'|'\\n'|'\\\\'|'\\\d+'"
   global y_last_newline
   lexem = t.value
   t.value = t.value[1:-1]
   if t.value[0] == '\\' and t.value[1] == '0':
      if len(t.value) == 2:       #it is \0
         if y_show_tokens:
            print("   ",t)
         return t
      else:
         lex_error("character literal does not allow leading zeros\n"+lexem,t)
   elif t.value[0] == '\\' and t.value[1] >= '0' and t.value[1] <= '9':
      b = int(t.value[1:])
      if b > 255:
        lex_error("character literal must have values 0..255\n"+lexem,t)
      else:
         if y_show_tokens:
            print("   ",t)
         return t                 # it is \255
   else:
      if y_show_tokens:
         print("   ",t)
      return t                    # it is a or \n or \\

def t_ID_AT(t):
   r'[a-zA-Z_][a-zA-Z_0-9]*[ ]*&'
   for i in range(len(t.value)):
      if t.value[i] == ' ' or t.value[i] == '&':
         j = i
         break
   id = t.value[:j]
   if len(id) > 256:
      lex_error('identifier {} too long'.format(id),t)
   elif id == 'bool':
      t.type = 'BOOL_AT'
      t.value = id+'&'
   elif id == 'char':
      t.type = 'CHAR_AT'
      t.value = id+'&'
   elif id == 'string':
      t.type = 'STRING_AT'
      t.value = id+'&'
   elif id == 'int':
      t.type = 'INT_AT'
      t.value = id+'&'
   elif id == 'float':
      t.type = 'FLOAT_AT'
      t.value = id+'&'
   elif is_protected(id):
      lex_error('identifier {} is protected, cannot be used in this context'.format(id),t)
   elif is_reserved(id):
      lexer.lexpos = t.lexpos + len(id)
      t.type = reserved.get(id)
      t.value = id
   else:
      # leave type ID_AT
      t.value = id+'&'
   if y_show_tokens:
      print("   ",t)
   return t

def t_ID_DOT(t):
   r'[a-zA-Z_][a-zA-Z_0-9]*\.'
   id = t.value[:-1]
   if len(id) > 256:
     lex_error('identifier {} too long'.format(id),t)
   elif id == 'parent':
      t.type = 'PARENT_DOT'
      t.value = id+'.'
   elif id == 'fin':
      t.type = 'FIN_DOT'
      t.value = id+'.'
   elif id == 'fout':
      t.type = 'FOUT_DOT'
      t.value = id+'.'
   elif is_protected(id):
      lex_error('identifier {} is protected, cannot be used in this context'.format(id),t)
   elif is_reserved(id):
      lexer.lexpos = t.lexpos + len(id)
      t.type = reserved.get(id)
      t.value = id
   else:
      # leave t.type as ID_DOT
      t.value = id+'.'
   if y_show_tokens:
      print("   ",t)
   return t


def t_ID_COLON(t):
   r'[a-zA-Z_][a-zA-Z_0-9]*[ ]*:'
   for i in range(len(t.value)):
      if t.value[i] == ' ' or t.value[i] == ':':
         j = i
         break
   id = t.value[:j]
   if len(id) > 256:
      lex_error('identifier {} too long'.format(id),t)
   elif is_protected(id):
      lex_error('identifier {} is protected, cannot be used in this context'.format(id),t)
   elif is_reserved(id):
      lexer.lexpos = t.lexpos + len(id)
      t.type = reserved.get(id)
      t.value = id
   else:
      t.value = id+':'
   if y_show_tokens:
      print("   ",t)
   return t


def t_ID_LP(t):
   r'[a-zA-Z_][a-zA-Z_0-9]*[ ]*\('
   for i in range(len(t.value)):
      if t.value[i] == ' ' or t.value[i] == '(':
         j = i
         break
   id = t.value[:j]
   if len(id) > 256:
      lex_error('identifier {} too long'.format(id),t)
   elif id == 'bool':
      t.type = 'BOOL_LP'
      t.value = id+'('
   elif id == 'char':
      t.type = 'CHAR_LP'
      t.value = id+'('
   elif id == 'string':
      t.type = 'STRING_LP'
      t.value = id+'('
   elif id == 'int':
      t.type = 'INT_LP'
      t.value = id+'('
   elif id == 'float':
      t.type = 'FLOAT_LP'
      t.value = id+'('
   elif id == 'idof':
      t.type = 'IDOF_LP'
      t.value = id+'('
   elif id == 'sizeof':
      t.type = 'SIZEOF_LP'
      t.value = id+'('
   elif id == 'typeof':
      t.type = 'TYPEOF_LP'
      t.value = id+'('
   elif is_protected(id):
      lex_error('identifier {} is protected, cannot be used in this context'.format(id),t)
   elif is_reserved(id):
      lexer.lexpos = t.lexpos + len(id)
      t.type = reserved.get(id)
      t.value = id
   else:
      t.value = id+'('
   if y_show_tokens:
      print("   ",t)
   return t

def t_ID_LS(t):
   r'[a-zA-Z_][a-zA-Z_0-9]*[ ]*\['
   for i in range(len(t.value)):
      if t.value[i] == ' ' or t.value[i] == '[':
         j = i
         break
   id =t.value[:j]
   if len(id) > 256:
      lex_error('identifier {} too long'.format(id),t)
   elif id == 'bool':
      t.type = 'BOOL_LS'
      t.value = id+'['
   elif id == 'char':
      t.type = 'CHAR_LS'
      t.value = id+'['
   elif id == 'string':
      t.type = 'STRING_LS'
      t.value = id+'['
   elif id == 'int':
      t.type = 'INT_LS'
      t.value = id+'['
   elif id == 'float':
      t.type = 'FLOAT_LS'
      t.value = id+'['
   elif is_protected(id):
      lex_error('identifier {} is protected, cannot be used in this context'.format(id),t)
   elif is_reserved(id):
      lexer.lexpos = t.lexpos + len(id)
      t.type = reserved.get(id)
      t.value = id
   else:
      t.value = id+'['
   if y_show_tokens:
      print("   ",t)
   return t


def t_ID(t):
   r'[a-zA-Z_][a-zA-Z_0-9]*'
   id = t.value
   if len(id) > 256:
      lex_error('identifier {} too long'.format(id),t)  
   elif is_protected(id):
      lex_error('identifier {} is protected, cannot be used in this context'.format(id),t)
   else:
      t.type = reserved.get(t.value,'ID')
   if y_show_tokens:
      print("   ",t)
   return t


def strcmp(s1,s2,a):
   for i in range(a):
      if s1[i] == s2[i]:
         continue
      return int(s1[i])-int(s2[i])
   return 0


# range ±2.23e+10^-308 to ±1.79e+10^308
def t_FLOAT_LIT(t):
   r'\d*\.\d*'
   global y_last_newline
   lexem = t.value
   a = len(t.value)
   if a == 1:
      lex_error("float literal cannot have leading zeros\n"+lexem,t)
   #find decimal point
   for i in range(len(t.value)):
      if t.value[i] == '.':
         dot = i
   if dot == 0:
      left = '0'
   else:
      left = t.value[:dot]
   if dot == a-1:
      right = '0'
   else:
      right = t.value[dot+1:]
   if left[0] == '0' and len(left) > 1:
      lex_error("float literal cannot have leading zeros\n"+lexem,t)
   x = float(left+'.'+right)
   if x < 2.23e-308:
      lex_error('float literal too small\n'+lexem,t)
   if x > 1.79e+308:
      lex_error('float literal too big\n'+lexem,t)
   t.value = float(left+'.'+right)
   if y_show_tokens:
      print("   ",t)
   return t

def t_INT_LIT(t):
   r'\d+'
   global y_last_newline
   lexem = t.value
   b = len(t.value)
   if b > 1:
      if t.value[0] == '0' and t.value[1] == '0':
         lex_error("int literal cannot have leading zeros\n"+lexem,t)
   if b > 19:
      lex_error("int literal too long\n"+lexem,t)
   if b == 19:
      if strcmp(t.value,'9223372036854775807',b) > 0:
         lex_error("int literal too big\n"+lexem,t)
   t.value = int(t.value)
   if y_show_tokens:
      print("   ",t)
   return t


def t_newline(t):
   r'\n+'
   global y_last_newline
   t.lexer.lineno += t.value.count("\n")
   y_last_newline = lexer.lexpos-1
   if y_show_tokens:
      print("    NEWLINE")


def t_error(t):
   global y_last_newline
   t.lexer.skip(1)
   m1 = "[{},{}]:".format(t.lineno,t.lexpos - y_last_newline)
   m2 = "Illegal character '{}'".format(t.value[0])
   print(m1,m2)
   print('offending line:\n {',end='')
   show_line(t.lineno)
   print('}')
   return

def lex_error(message,t):
   global y_last_newline
   p = t.lexpos - y_last_newline
   m1="[{},{}]:".format(t.lineno,t.lexpos - y_last_newline)
   print(m1,message)
   print('offending line:\n {',end='')
   show_line(t.lineno)
   print('}')
   sys.exit(0)

def show_line(lineno):
    if lineno == 1:
        for i in lexer.lexdata:
            if i == '\n':
                break
            else:
                print(i,end='')
        print()
        return

    count = 0
    target = False
    lineno = lineno-1
    for i in range(len(lexer.lexdata)):
        if lexer.lexdata[i] == '\n':
            if target:
                return
            else:
                count += 1
                if count == lineno:
                    target = True
                continue
                #endif
            #endif
        else:
            if target:
                print(lexer.lexdata[i],end='')
            continue
        #endif
    #endfor
#end show_line


lexer = lex.lex()
