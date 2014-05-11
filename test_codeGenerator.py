import compiler
from StringIO import StringIO
from unittest import TestCase
from compier import CodeGenerator
from util import flatten_expression, show_expression

__author__ = 'shengyu'


class TestCodeGenerator(TestCase):
    def test_flatten_to_atomic(self):
        ast = compiler.parse('1')
        flatten_expression(ast)
        expect = ''
        self.assertEquals(expect, show_expression(ast))

        ast = compiler.parse('a = 1')
        flatten_expression(ast)
        expect = 'a = 1\n'
        self.assertEquals(expect, show_expression(ast))

        ast = compiler.parse('input()')
        flatten_expression(ast)
        expect = 'tmp0 = input()\n'
        self.assertEquals(expect, show_expression(ast))

        ast = compiler.parse('input() + 20')
        flatten_expression(ast)
        expect = (
            'tmp0 = input()\n'
            'tmp1 = tmp0 + 20\n'
        )
        self.assertEquals(expect, show_expression(ast))

        ast = compiler.parse('print 1')
        flatten_expression(ast)
        expect = 'print 1\n'
        self.assertEquals(expect, show_expression(ast))

        ast = compiler.parse('print 1 + input()')
        flatten_expression(ast)
        expect = (
            'tmp0 = input()\n'
            'tmp1 = 1 + tmp0\n'
            'print tmp1\n'
        )
        self.assertEquals(expect, show_expression(ast))

        ast = compiler.parse('print -1 + input()')
        flatten_expression(ast)
        expect = (
            'tmp0 = -1\n'
            'tmp1 = input()\n'
            'tmp2 = tmp0 + tmp1\n'
            'print tmp2\n'
        )
        self.assertEquals(expect, show_expression(ast))

        ast = compiler.parse('print -input() + 20')
        flatten_expression(ast)
        expect = (
            'tmp0 = input()\n'
            'tmp1 = -tmp0\n'
            'tmp2 = tmp1 + 20\n'
            'print tmp2\n'
        )
        self.assertEquals(expect, show_expression(ast))

    def test_code_generation(self):
        codegen = CodeGenerator()
        output = StringIO()

        ast = compiler.parse('print -input() + 20')
        flatten_expression(ast)
        output.truncate(0)
        codegen.generate(ast, output)
        expect = (
            '\tcall input\n'
            '\tmovl %eax, -4(%ebp)\n'
            '\tmovl -4(%ebp), %eax\n'
            '\tnegl %eax\n'
            '\tmovl %eax, -8(%ebp)\n'
            '\tmovl -8(%ebp), %eax\n'
            '\taddl $20, %eax\n'
            '\tmovl %eax, -12(%ebp)\n'
            '\tpushl -12(%ebp)\n'
            '\tcall print_int_nl\n'
            '\taddl $4, %esp\n'
        )
        self.assertEquals(expect, output.getvalue())

        output.close()

