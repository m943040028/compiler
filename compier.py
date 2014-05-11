import re
from compiler.ast import *

__author__ = 'shengyu'


def _map_variable_name_to_stack_offset(n):
    if not isinstance(n, AssName) and not isinstance(n, Name):
        raise TypeError("given type is not a AssName or Name")

    m = re.search('.*([0-9]+)$', n.name)

    if m is None:
        raise NameError("given variable name is not match with tmp[0-9]+")

    return -(int(m.group(1)) + 1) * 4


class CodeGenerator:
    def __init__(self):
        pass

    @staticmethod
    def _generate_store_variable(n, reg, output):
        output.write('\tmovl %s, %d(%%ebp)\n' % (reg, _map_variable_name_to_stack_offset(n)))

    @staticmethod
    def _generate_load_variable(n, reg, output):
        output.write('\tmovl %d(%%ebp), %s\n' % (_map_variable_name_to_stack_offset(n), reg))

    def generate(self, n, output):
        if isinstance(n, Module):
            self.generate(n.node, output)
        if isinstance(n, Stmt):
            for x in n.nodes:
                self.generate(x, output)
        if isinstance(n, Assign):
            self.generate(n.expr, output)
            self._generate_store_variable(n.nodes[0], '%eax', output)
        if isinstance(n, UnarySub):
            self._generate_load_variable(n.expr, '%eax', output)
            output.write('\tnegl %eax\n')
        if isinstance(n, CallFunc):
            output.write('\tcall %s\n' % n.node.name)
        if isinstance(n, Add):
            if isinstance(n.left, Const):
                output.write('\tmovl %%%d, %%eax\n' % n.left.name)
            elif isinstance(n.left, Name):
                self._generate_load_variable(n.left, '%eax', output)
            if isinstance(n.right, Const):
                output.write('\taddl $%d, %%eax\n' % n.right.value)
            elif isinstance(n.left, Name):
                self._generate_load_variable(n.left, '%ebx', output)
                output.write('\taddl %ebx, %%eax\n')
        if isinstance(n, Printnl):
            output.write('\tpushl %d(%%ebp)\n' % _map_variable_name_to_stack_offset(n.nodes[0]))
            output.write('\tcall print_int_nl\n')
            output.write('\taddl $4, %esp\n')
