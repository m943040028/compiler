import compiler
from unittest import TestCase
from util import flatten_expression, show_expression

__author__ = 'shengyu'


class TestCodeGen(TestCase):
    def test_flatten_to_atomic(self):

        ast = compiler.parse('1')
        flatten_expression(ast)
        expect = ''
        self.assertEquals(show_expression(ast), expect)

        ast = compiler.parse('a = 1')
        flatten_expression(ast)
        expect = 'a = 1\n'
        self.assertEquals(show_expression(ast), expect)

        # check if this is Correct !
        ast = compiler.parse('input()')
        flatten_expression(ast)
        expect = 'tmp0 = input()\n'
        self.assertEquals(show_expression(ast), expect)

        ast = compiler.parse('print 1')
        flatten_expression(ast)
        expect = 'print 1\n'
        self.assertEquals(show_expression(ast), expect)

        ast = compiler.parse('print 1 + input()')
        flatten_expression(ast)
        expect = (
            'tmp0 = input()\n'
            'tmp1 = 1 + tmp0\n'
            'print tmp1\n'
        )
        self.assertEquals(show_expression(ast), expect)

        ast = compiler.parse('print -1 + input()')
        flatten_expression(ast)
        expect = (
            'tmp0 = -1\n'
            'tmp1 = input()\n'
            'tmp2 = tmp0 + tmp1\n'
            'print tmp2\n'
        )
        self.assertEquals(show_expression(ast), expect)

        ast = compiler.parse('print -input() + 20')
        flatten_expression(ast)
        expect = (
            'tmp0 = -input()\n'
            'tmp1 = tmp0 + 20\n'
            'print tmp1\n'
        )
        self.assertEquals(show_expression(ast), expect)