#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Tests for tagger.
"""

import unittest
from quepy import tagger


class TestTagger(unittest.TestCase):
    def test_tagset_unicode(self):
        for tag in tagger.PENN_TAGSET:
            self.assertIsInstance(tag, str)

    def test_word_encoding(self):
        word = tagger.Word(token="æßđħłłþłłł@æµß",
                           lemma="ŧłþłßæ#¶ŋħ~#~@",
                           pos="øĸŋøħþ€ĸłþ€øæ«»¢")

        self.assertIsInstance(word.token, str)
        self.assertEqual(word.token, "æßđħłłþłłł@æµß")
        self.assertIsInstance(word.lemma, str)
        self.assertEqual(word.lemma, "ŧłþłßæ#¶ŋħ~#~@")
        self.assertIsInstance(word.pos, str)
        self.assertEqual(word.pos, "øĸŋøħþ€ĸłþ€øæ«»¢")

    def test_word_wrong_encoding(self):
        # Token not unicode
        self.assertRaises(ValueError, tagger.Word, "æßđħłłþłłł@æµß".encode(),
                          "ŧłþłßæ#¶ŋħ~#~@", "øĸŋøħþ€ĸłþ€øæ«»¢")
        # Lemma not unicode
        self.assertRaises(ValueError, tagger.Word, "æßđħłłþłłł@æµß",
                          "ŧłþłßæ#¶ŋħ~#~@".encode(), "øĸŋøħþ€ĸłþ€øæ«»¢")
        # Pos not unicode
        self.assertRaises(ValueError, tagger.Word, "æßđħłłþłłł@æµß",
                          "ŧłþłßæ#¶ŋħ~#~@", "øĸŋøħþ€ĸłþ€øæ«»¢".encode())

    def test_word_attrib_set(self):
        word = tagger.Word("æßđħłłþłłł@æµß")
        word.lemma = "ŧłþłßæ#¶ŋħ~#~@"
        word.pos = "øĸŋøħþ€ĸłþ€øæ«»¢"

        self.assertIsInstance(word.token, str)
        self.assertEqual(word.token, "æßđħłłþłłł@æµß")
        self.assertIsInstance(word.lemma, str)
        self.assertEqual(word.lemma, "ŧłþłßæ#¶ŋħ~#~@")
        self.assertIsInstance(word.pos, str)
        self.assertEqual(word.pos, "øĸŋøħþ€ĸłþ€øæ«»¢")

    def test_word_wrong_attrib_set(self):
        word = tagger.Word("æßđħłłþłłł@æµß")

        # Token not unicode
        self.assertRaises(ValueError, setattr, word, "token", "æßđħłłþłłł@æµß".encode())
        # Lemma not unicode
        self.assertRaises(ValueError, setattr, word, "lemma", "ŧłþłßæ#¶ŋħ~#~@".encode())
        # Pos not unicode
        self.assertRaises(ValueError, setattr, word, "pos", "øĸŋøħþ€ĸłþ€øæ«»¢".encode())
