from compiler.ast import Printnl, Add, Const

__author__ = 'shengyu'

precedence = (
    ('nonassoc', 'PRINT'),
    ('left', 'PLUS')
)


def p_print_statement(t):
    'statement : PRINT expression'
    t[0] = Printnl(t[2], None)


def p_plus_expression(t):
    'expression : expression PLUS expression'
    t[0] = Add(t[1], t[3])


def p_int_expression(t):
    'expression : INT'
    t[0] = Const(t[1])


def p_error(t):
    print "Syntax error at '%s" % t.value


import ply.yacc as yacc

yacc.yacc()