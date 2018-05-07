#!/usr/bin/env python

import ast


def read_setup_details(data):
    parsed = ast.parse(data)
    call = find_setup_call(parsed)
    name = find_keyword(call, 'name')
    version = find_keyword(call, 'version')

    return name, version


def find_setup_call(tree):
    finder = CallFinder()
    finder.visit(tree)

    for node in finder.calls:
        if node.func.id == 'setup':
            return node
    raise ValueError('Could not find call to setup in setup.py file')


class CallFinder(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):  # pylint: disable=invalid-name
        self.calls.append(node)


def find_keyword(call, arg):
    for keyword in call.keywords:
        if keyword.arg == arg:
            return keyword.value.s
    raise ValueError('Could not find {arg} in call keywords'.format(arg=arg))
