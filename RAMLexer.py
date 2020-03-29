import ply.lex as lex


tokens = ['INCREMENT', 'DECREMENT', 'CLEAR', 'MOVE', 'JUMP', 'CONTINUE', 'LABEL',
          'REGISTER', 'LABEL_ABOVE', 'LABEL_BELOW', 'EQUAL', 'NUMBER', 'COMMA']

t_INCREMENT = r'[iI][nN][cC]'
t_DECREMENT = r'[dD][eE][cC]'
t_CLEAR = r'[cC][lL][rR]'
t_MOVE = r'[mM][oO][vV]'
t_JUMP = r'[jJ][mM][pP]'
t_CONTINUE = r'[cC][oO][nN][tT][iI][nN][uU][eE]'
t_REGISTER = r'[rR][1-9][0-9]*'
t_LABEL_ABOVE = r'[nN][0-9]+[aA]'
t_LABEL_BELOW = r'[nN][0-9]+[bB]'
t_LABEL = r'[nN][0-9]+'
t_EQUAL = r'='
t_COMMA = r','


t_ignore = " \r\t\n"
t_ignore_COMMENT = r'\#.*'

def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    #t.lexer.skip(1)
    raise Exception('LEXER ERROR')


lexer = lex.lex()

## Test it out
#data = '''
## Program to add two numbers
## inputs are in r1 and r2
## output, as always, is in r1
##
## initialize input registers
#r1 = 9
#R2 = 3
##
## begin program
#n0 R2 JMP N1b
#   INC R1
#   DEC R2
#    JMP N0a
#N1 CONTINUE'''
## Give the lexer some input
#lexer.input(data)
## Tokenize
#while True:
#    tok = lexer.token()
#    if not tok:
#        break      # No more input
#    print(tok)