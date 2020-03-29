import ply.yacc as yacc
from RAMLexer import tokens


def p_progStart(p):
    'progStart : inputs codes'
    p[0] = [dict(p[1]), p[2]]


def p_inputs_1(p):
    'inputs : input inputs'
    p[0] = p[1], p[2]


def p_inputs_2(p):
    'inputs : input'
    p[0] = p[1]


def p_inputs_3(p):
    'input : REGISTER EQUAL NUMBER'
    p[0] = (p[1].upper(), p[3])


def p_codes_1(p):
    'codes : codes code'
    #p[0] = p[2], p[1]
    p[0] = p[1]
    p[0].append(p[2])

def p_codes_2(p):
    'codes : code'
    p[0] = [p[1]]


def p_codes_3(p):
    'code : LABEL code'
    p[0] = {'label' : p[1].upper(),
            'code' : p[2]}


def p_ram_1(p):
    'code : INCREMENT REGISTER'
    p[0] = {'opcode' : 'inc',
            'register' : p[2].upper()}


def p_ram_2(p):
    'code : DECREMENT REGISTER'
    p[0] = {'opcode' : 'dec',
            'register' : p[2].upper()}


def p_ram_3(p):
    'code : CLEAR REGISTER'
    p[0] = {'opcode' : 'clr',
            'register' : p[2].upper()}


def p_ram_4(p):
    'code : MOVE REGISTER COMMA REGISTER'
    p[0] = {'opcode' : 'mov',
            'register1' : p[2].upper(),
            'register2' : p[4].upper()}


def p_jump_abv(p):
    'jumpa : JUMP LABEL_ABOVE'
    p[0] = p[2].upper()


def p_jump_bel(p):
    'jumpb : JUMP LABEL_BELOW'
    p[0] = p[2].upper()


def p_ram_5a(p):
    'code : jumpa'
    p[0] = {'opcode' : 'jmpa',
            'label_acc' : p[1].upper()}


def p_ram_5b(p):
    'code : jumpb'
    p[0] = {'opcode' : 'jmpb',
            'label_acc' : p[1].upper()}


def p_ram_6a(p):
    'code : REGISTER jumpa'
    p[0] = {'opcode' : 'jmpa',
            'register' : p[1].upper(),
            'label_acc' : p[2].upper()}


def p_ram_6b(p):
    'code : REGISTER jumpb'
    p[0] = {'opcode' : 'jmpb',
            'register' : p[1].upper(),
            'label_acc' : p[2].upper()}


def p_ram_7(p):
    'code : CONTINUE'
    p[0] = {'opcode': p[1].upper()}



def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc()