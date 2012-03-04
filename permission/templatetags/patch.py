# vim: set fileencoding=utf-8 :
"""
short module explanation


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
License:
    The MIT License (MIT)

    Copyright (c) 2012 Alisue allright reserved.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to
    deal in the Software without restriction, including without limitation the
    rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
    sell copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
    IN THE SOFTWARE.

"""
from __future__ import with_statement
from distutils.version import StrictVersion
from django import get_version

if StrictVersion(get_version()) < '1.4':
    from django.template import Node
    from django.template import NodeList
    from django.template import VariableDoesNotExist
    from django.template import TemplateSyntaxError
    from django.template.base import TextNode
    # copied from django 1.4b
    class IfNode(Node):
        def __init__(self, conditions_nodelists):
            self.conditions_nodelists = conditions_nodelists
        def __repr__(self):
            return "<IfNode>"
        def __iter__(self):
            for _, nodelist in self.conditions_nodelists:
                for node in nodelist:
                    yield node
        @property
        def nodelist(self):
            return NodeList(node for _, nodelist in self.conditions_nodelists for node in nodelist)
        def render(self, context):
            for condition, nodelist in self.conditions_nodelists:
                if condition is not None:           # if / elif clause
                    try:
                        match = condition.eval(context)
                    except VariableDoesNotExist:
                        match = None
                else:                               # else clause
                    match = True
                if match:
                    return nodelist.render(context)
            return ''
    # copied from django 1.4b
    def parse(self, parse_until=None):
        if parse_until is None:
            parse_until = []
        nodelist = self.create_nodelist()
        while self.tokens:
            token = self.next_token()
            # Use the raw values here for TOKEN_* for a tiny performance boost.
            if token.token_type == 0: # TOKEN_TEXT
                self.extend_nodelist(nodelist, TextNode(token.contents), token)
            elif token.token_type == 1: # TOKEN_VAR
                if not token.contents:
                    self.empty_variable(token)
                filter_expression = self.compile_filter(token.contents)
                var_node = self.create_variable_node(filter_expression)
                self.extend_nodelist(nodelist, var_node, token)
            elif token.token_type == 2: # TOKEN_BLOCK
                try:
                    command = token.contents.split()[0]
                except IndexError:
                    self.empty_block_tag(token)
                if command in parse_until:
                    # put token back on token list so calling
                    # code knows why it terminated
                    self.prepend_token(token)
                    return nodelist
                # execute callback function for this tag and append
                # resulting node
                self.enter_command(command, token)
                try:
                    compile_func = self.tags[command]
                except KeyError:
                    self.invalid_block_tag(token, command, parse_until)
                try:
                    compiled_result = compile_func(self, token)
                except TemplateSyntaxError, e:
                    if not self.compile_function_error(token, e):
                        raise
                self.extend_nodelist(nodelist, compiled_result, token)
                self.exit_command()
        if parse_until:
            self.unclosed_block_tag(parse_until)
        return nodelist
    def parser_patch(instance):
        instance.__class__.parse = parse
        return instance
else:
    from django.template.defaulttags import IfNode
    parser_patch = lambda instance: instance

