__author__ = 'shengyu'

tokens = ('PRINT', 'INT', 'PLUS')

t_PRINT = r'print'
t_PLUS = r'\+'


def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "integer value too large", t.value
        t.value = 0
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print "Illegal character '%s" % t.value[0]
    t.lexer.skip(1)

import ply.lex as lex
lex.lex()