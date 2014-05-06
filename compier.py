import sys

__author__ = 'shengyu'

import compiler
from compiler.ast import *


class VariableAllocator:
    def __init__(self):
        self.count = -1

    def new_variable(self):
        self.count += 1
        return "tmp" + str(self.count)


def flatten_expression(ast):
    alloc = VariableAllocator()
    _flatten_expression_recursively(ast, alloc)


def _flatten_expression_recursively(n, alloc):
    if isinstance(n, Module):
        _flatten_expression_recursively(n.node, alloc)
    elif isinstance(n, Stmt):
        [_flatten_expression_recursively(x, alloc) for x in n.nodes]
    elif isinstance(n, Printnl):
        operand = _flatten_expression_recursively(n.nodes[0], alloc)
        sys.stdout.write('print %s\n' % operand)
    elif isinstance(n, Add):
        left_operand = _flatten_expression_recursively(n.left, alloc)
        right_operand = _flatten_expression_recursively(n.right, alloc)
        new_var = alloc.new_variable()
        sys.stdout.write('%s = %s + %s\n' % (new_var, left_operand, right_operand))
        return new_var
    elif isinstance(n, CallFunc):
        new_var = alloc.new_variable()
        sys.stdout.write('%s = ' % new_var)
        _flatten_expression_recursively(n.node, alloc)
        sys.stdout.write('(')
        for x in n.args:
            sys.stdout.write(x + ',')
        sys.stdout.write(')\n')
        return new_var

    elif isinstance(n, Name):
        sys.stdout.write(n.name)
    elif isinstance(n, UnarySub):
        operand = _flatten_expression_recursively(n.expr, alloc)
        new_var = alloc.new_variable()
        sys.stdout.write('%s = -%s\n' % (new_var, operand))
        return new_var


ast = compiler.parse('print - input() + input()')

flatten_expression(ast)
