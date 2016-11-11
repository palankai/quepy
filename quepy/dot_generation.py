# -*- coding: utf-8 -*-

"""
Dot generation code.
"""

import random
from quepy.expression import isnode
from quepy.dsl import IsRelatedTo, HasKeyword
from quepy.encodingpolicy import assert_valid_encoding


def escape(x, add_quotes=True):
    x = str(x)
    x = x.replace(" ", "_")
    x = x.replace("\n", "")
    x = x.replace("\00", "")
    x = x.replace("[", "")
    x = x.replace("]", "")
    x = x.replace("\\", "")
    if x.count("\""):
        x = x.replace("\"", "\\\"")
        if add_quotes:
            x = '"' + x + '"'
    return x


def adapt(x):
    if isnode(x):
        x = "x{}".format(x)
        return x
    if isinstance(x, (str, bytes)):
        assert_valid_encoding(x)
        x = escape(x)
        if x.startswith("\""):
            return x
        return '"{}"'.format(x)
    return str(x)


def expression_to_dot(e):
    d = {"rdf:type": dot_type,
         HasKeyword.relation: dot_keyword,
         IsRelatedTo: lambda x, y: dot_arc(x, "", y)}
    s = "digraph G {{\n{0} [shape=house];\n{1}\n}}\n"
    xs = []
    for node in e.iter_nodes():
        for relation, other in e.iter_edges(node):
            node1 = adapt(node)
            node2 = adapt(other)
            relation = escape(relation, add_quotes=False)

            if relation in d:
                x = d[relation](node1, node2)
            else:
                x = dot_arc(node1, relation, node2)
            xs.append(x)
    return None, s.format(adapt(e.head), "".join(xs))


def dot_arc(a, label, b):
    assert " " not in a and " " not in b
    assert "\n" not in a + label + b
    return "{0} -> {1} [label=\"{2}\"];\n".format(a, b, label)


def dot_type(a, t):
    s = "{0} [shape=box];\n".format(t)
    return s + "{0} -> {1} [color=red, arrowhead=empty];".format(a, t)


def dot_attribute(a, key):
    blank = id(a)
    s = "{0} [shape=none label={1}];\n".format(blank, key)
    return s + "{0} -> {1};".format(a, blank)


def dot_keyword(a, key):
    blank = "{0:.30f}".format(random.random())
    blank = "blank" + blank.replace(".", "")
    s = "{0} [shape=none label={1}];\n".format(blank, key)
    return s + "{0} -> {1} [style=dashed];".format(a, blank)


def dot_fixed_type(a, fixedtype):
    blank = "{0:.30f}".format(random.random())
    blank = "blank" + blank.replace(".", "")
    s = "{0} [shape=box label={1}];\n".format(blank, fixedtype)
    return s + "{0} -> {1} [color=red, arrowhead=empty];".format(a, blank)
