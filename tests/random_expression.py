# -*- coding: utf-8 -*-
import random
from quepy.expression import Expression


def random_data(only_ascii=False):
    data = []
    first = True
    while first or 1 / 20.0 < random.random():
        first = False
        if only_ascii:
            c = chr(random.randint(33, 126))
            data.append(c)
            continue
        x = random.random()
        if 0.1 > x:
            c = random.choice(" ./\n")
        elif 0.50 > x:
            c = chr(random.randint(65, 122))
        elif 0.85 > x:
            c = chr(random.randint(0, 127))
        else:
            #i = random.randint(0,65535)
            #c = chr(i)
            c = random_utf8_seq().decode('utf-8')
        data.append(c)
    return "".join(data)

# Credit: http://stackoverflow.com/a/1477572/1343862

def byte_range(first, last):
    return list(range(first, last+1))

first_values = byte_range(0x00, 0x7F) + byte_range(0xC2, 0xF4)
trailing_values = byte_range(0x80, 0xBF)

def random_utf8_seq():
    first = random.choice(first_values)
    if first <= 0x7F:
        return bytes([first])
    elif first <= 0xDF:
        return bytes([first, random.choice(trailing_values)])
    elif first == 0xE0:
        return bytes([first, random.choice(byte_range(0xA0, 0xBF)), random.choice(trailing_values)])
    elif first == 0xED:
        return bytes([first, random.choice(byte_range(0x80, 0x9F)), random.choice(trailing_values)])
    elif first <= 0xEF:
        return bytes([first, random.choice(trailing_values), random.choice(trailing_values)])
    elif first == 0xF0:
        return bytes([first, random.choice(byte_range(0x90, 0xBF)), random.choice(trailing_values), random.choice(trailing_values)])
    elif first <= 0xF3:
        return bytes([first, random.choice(trailing_values), random.choice(trailing_values), random.choice(trailing_values)])
    elif first == 0xF4:
        return bytes([first, random.choice(byte_range(0x80, 0x8F)), random.choice(trailing_values), random.choice(trailing_values)])


def random_relation(only_ascii=False):
    data = random_data(only_ascii)
    data = data.replace(" ", "")
    if random.random() > 0.05:
        return data

    class UnicodeableDummy(object):
        def __unicode__(self):
            return data
        def __str__(self):
            return data
    return UnicodeableDummy()


def random_expression(only_ascii=False):
    """
    operations: new node, add data, decapitate, merge
    """
    mean_size = 20
    xs = [40.0, 30.0, 50.0, 20.0]
    xs = [x * (1.0 - random.random()) for x in xs]
    assert all(x != 0 for x in xs)
    new_node, add_data, decapitate, _ = [x / sum(xs) for x in xs]
    expressions = [Expression(), Expression(), Expression(), Expression()]
    while len(expressions) != 1:
        if (1.0 / mean_size) < random.random():
            # Will start to merge more and will not create new nodes
            new_node = 0.0
        # Choose action
        r = random.random()
        if r < new_node:
            # New expression
            expressions.append(Expression())
        elif r < add_data + new_node:
            # Add data
            e = random.choice(expressions)
            e.add_data(random_relation(only_ascii), random_data(only_ascii))
        elif r < decapitate + add_data + new_node:
            # Decapitate
            e = random.choice(expressions)
            e.decapitate(random_relation(only_ascii),
                         reverse=(0.25 < random.random()))
        elif len(expressions) != 1:
            # Merge
            random.shuffle(expressions)
            e2 = expressions.pop()
            e1 = expressions[-1]
            e1 += e2
    return expressions[0]
