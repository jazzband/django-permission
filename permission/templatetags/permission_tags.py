# vim: set fileencoding=utf-8 :
"""
templatetags


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
from django.conf import settings
from django import template
from django.template import TemplateSyntaxError
from django.template import VariableDoesNotExist
from django.template.smartif import infix
from django.template.smartif import IfParser
from django.template.smartif import OPERATORS
from django.template.defaulttags import Node
from django.template.defaulttags import NodeList
from django.template.defaulttags import TemplateLiteral

from permission.templatetags.patch import IfNode
from permission.templatetags.patch import parser_patch

register = template.Library()

def of_operator(context, x, y):
    return x.eval(context), y.eval(context)

def has_operator(context, x, y):
    user = x.eval(context)
    perm = y.eval(context)
    if isinstance(perm, (list, tuple)):
        perm, obj = perm
    else:
        obj = None
    return user.has_perm(perm, obj)

EXTRA_OPERATORS = {
    'of': infix(20, of_operator),
    'has': infix(10, has_operator),
}
EXTRA_OPERATORS.update(OPERATORS)
# Assign 'id' to each:
for key, op in EXTRA_OPERATORS.items():
    op.id = key

class PermissionIfParser(IfParser):
    OPERATORS = EXTRA_OPERATORS

    def translate_token(self, token):
        try:
            op = self.OPERATORS[token]
        except (KeyError, TypeError):
            return self.create_var(token)
        else:
            return op()

class TemplatePermissionIfParser(PermissionIfParser):
    error_class = TemplateSyntaxError

    def __init__(self, parser, *args, **kwargs):
        self.template_parser = parser
        super(TemplatePermissionIfParser, self).__init__(*args, **kwargs)

    def create_var(self, value):
        return TemplateLiteral(self.template_parser.compile_filter(value), value)


@register.tag('permission')
def do_permissionif(parser, token):
    # patch parser for django 1.3.1
    parser = parser_patch(parser)

    bits = token.split_contents()
    ELIF = "el%s" % bits[0]
    ELSE = "else"
    ENDIF = "end%s" % bits[0]

    # {% if ... %}
    bits = bits[1:]
    condition = do_permissionif.Parser(parser, bits).parse()
    nodelist = parser.parse((ELIF, ELSE, ENDIF))
    conditions_nodelists = [(condition, nodelist)]
    token = parser.next_token()

    # {% elif ... %} (repeatable)
    while token.contents.startswith(ELIF):
        bits = token.split_contents()[1:]
        condition = do_permissionif.Parser(parser, bits).parse()
        nodelist = parser.parse((ELIF, ELSE, ENDIF))
        conditions_nodelists.append((condition, nodelist))
        token = parser.next_token()

    # {% else %} (optional)
    if token.contents == ELSE:
        nodelist = parser.parse((ENDIF,))
        conditions_nodelists.append((None, nodelist))
        token = parser.next_token()

    # {% endif %}
    assert token.contents == ENDIF

    return IfNode(conditions_nodelists)
do_permissionif.Parser = TemplatePermissionIfParser

if settings.PERMISSION_REPLACE_BUILTIN_IF:
    register.tag('if', do_permissionif)

