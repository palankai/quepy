# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

import unittest
from quepy.expression import Expression
from quepy.dsl import HasKeyword, FixedRelation, FixedType, \
    FixedDataRelation


class TestDSL(unittest.TestCase):
    def test_fixed_relation(self):

        class MyFixedRelation(FixedRelation):
            relation = "uranium:blowtorch"

        empty = Expression()
        fixedinstance = MyFixedRelation(empty)

        head = fixedinstance.get_head()
        relations = [x[0] for x in fixedinstance.iter_edges(head)]

        self.assertIn("uranium:blowtorch", relations)

    def test_fixed_type(self):

        class MyFixedType(FixedType):
            fixedtype = "uranium:blowtorch"
            fixedtyperelation = "rdf:type"

        fixedinstance = MyFixedType()

        head = fixedinstance.get_head()
        edges = list(fixedinstance.iter_edges(head))

        self.assertEqual(len(edges), 1)
        self.assertIsInstance(edges[0][0], str)
        self.assertEqual(edges[0][0], "rdf:type")
        self.assertIsInstance(edges[0][1], str)
        self.assertEqual(edges[0][1], "uranium:blowtorch")

    def test_fixed_data_relation(self):

        class MyFixedDataRelation(FixedDataRelation):
            relation = "uranium:blowtorch"

        fixedinstance = MyFixedDataRelation("soplete")
        head = fixedinstance.get_head()
        edges = list(fixedinstance.iter_edges(head))

        self.assertEqual(len(edges), 1)
        self.assertIsInstance(edges[0][0], str)
        self.assertEqual(edges[0][0], "uranium:blowtorch")
        self.assertIsInstance(edges[0][1], str)
        self.assertEqual(edges[0][1], "soplete")

    def test_has_keyword(self):

        HasKeyword.relation = "uranium:keyword"
        keywordinstance = HasKeyword("soplete")

        head = keywordinstance.get_head()
        edges = list(keywordinstance.iter_edges(head))
        self.assertEqual(len(edges), 1)
        self.assertIsInstance(edges[0][0], str)
        self.assertEqual(edges[0][0], "uranium:keyword")
        self.assertIsInstance(edges[0][1], str)
        self.assertEqual(edges[0][1], 'soplete')

        # With language
        HasKeyword.language = "en"
        keywordinstance = HasKeyword("soplete")

        head = keywordinstance.get_head()
        edges = list(keywordinstance.iter_edges(head))
        self.assertEqual(len(edges), 1)
        self.assertIsInstance(edges[0][1], str)
        self.assertEqual(edges[0][1], '"soplete"@en')

        # With sanitize
        HasKeyword.sanitize = staticmethod(lambda x: x.upper())
        keywordinstance = HasKeyword("soplete")

        head = keywordinstance.get_head()
        edges = list(keywordinstance.iter_edges(head))
        self.assertEqual(len(edges), 1)
        self.assertIsInstance(edges[0][1], str)
        self.assertEqual(edges[0][1], '"SOPLETE"@en')


if __name__ == "__main__":
    unittest.main()
