#!/usr/bin/env python

import ast


def read_setup_details(data):
    parsed = ast.parse(data)
    call = _find_setup_call(parsed)
    name = _find_name(call)
    version = _find_version(call)
    scripts = _find_scripts(call)

    return name, version, scripts


def _find_setup_call(tree):
    finder = CallFinder()
    finder.visit(tree)

    for node in finder.calls:
        if 'id' not in dir(node.func):
            continue
        if node.func.id == 'setup':
            return node
    raise ValueError('Could not find call to setup in setup.py file')


class CallFinder(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):  # pylint: disable=invalid-name
        self.calls.append(node)


def _find_name(call):
    return _find_keyword(call, 'name').s


def _find_version(call):
    try:
        return _find_keyword(call, 'version').s
    except:  # pylint: disable=bare-except
        return None


def _find_scripts(call):
    try:
        scripts = _find_keyword(call, 'scripts') or []

        return [node.s for node in scripts.elts]
    except:  # pylint: disable=bare-except
        return []


def _find_keyword(call, arg):
    for keyword in call.keywords:
        if keyword.arg == arg:
            return keyword.value
    raise ValueError('Could not find {arg} in call keywords'.format(arg=arg))
