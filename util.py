__author__ = 'shengyu'

from compiler.ast import *


class VariableAllocator:
    def __init__(self):
        self.count = -1

    def new_variable(self):
        self.count += 1
        return "tmp" + str(self.count)


def flatten_expression(ast):
    alloc = VariableAllocator()
    _flatten_to_atomic(ast, alloc)


def _flatten_to_atomic(n, alloc):
    if isinstance(n, Module):
        _flatten_to_atomic(n.node, alloc)

    elif isinstance(n, Stmt):
        replaced_nodes = []
        for x in n.nodes:
            atomic_node, new_nodes = _flatten_to_atomic(x, alloc)
            replaced_nodes.extend(new_nodes)
            replaced_nodes.append(atomic_node)
        n.nodes = replaced_nodes

    elif isinstance(n, Printnl):
        atomic_node, new_nodes = _flatten_to_atomic(n.nodes[0], alloc)
        n.nodes[0] = atomic_node
        return n, new_nodes

    elif isinstance(n, Assign):
        atomic_node, new_nodes = _flatten_to_atomic(n.expr, alloc)
        n.expr = atomic_node
        return n, new_nodes

    elif isinstance(n, Add):
        new_nodes = []
        left_atomic, left_new_nodes = _flatten_to_atomic(n.left, alloc)
        right_atomic, right_new_nodes = _flatten_to_atomic(n.right, alloc)
        new_nodes.extend(left_new_nodes)
        new_nodes.extend(right_new_nodes)
        n.left = left_atomic
        n.right = right_atomic
        new_name = alloc.new_variable()
        new_assign = Assign([AssName(new_name, 'OP_ASSIGN')], n)
        new_nodes.append(new_assign)

        return Name(new_name), new_nodes

    elif isinstance(n, UnarySub) or isinstance(n, CallFunc):
        new_name = alloc.new_variable()
        new_assign = Assign([AssName(new_name, 'OP_ASSIGN')], n)

        return Name(new_name), [new_assign]

    elif isinstance(n, Discard):
        atomic_node, new_nodes = _flatten_to_atomic(n.expr, alloc)
        n.expr = atomic_node
        return n, new_nodes

    elif isinstance(n, Name):
        return n, []

    elif isinstance(n, Const):
        return n, []


def show_expression(n):
    if isinstance(n, Module):
        return show_expression(n.node)

    elif isinstance(n, Stmt):
        result = ""
        for x in n.nodes:
            result += show_expression(x)
        return result

    elif isinstance(n, Printnl):
        result = 'print '
        result += show_expression(n.nodes[0])
        result += '\n'
        return result

    elif isinstance(n, Assign):
        result = show_expression(n.nodes[0])
        result += ' = '
        result += show_expression(n.expr)
        result += '\n'
        return result

    elif isinstance(n, Add):
        result = show_expression(n.left)
        result += ' + '
        result += show_expression(n.right)
        return result

    elif isinstance(n, CallFunc):
        result = show_expression(n.node)
        result += '()'
        return result

    elif isinstance(n, UnarySub):
        result = '-'
        result += show_expression(n.expr)
        return result

    elif isinstance(n, Name) or isinstance(n, AssName):
        return n.name

    elif isinstance(n, Const):
        return str(n.value)

    elif isinstance(n, Discard):
        return ""