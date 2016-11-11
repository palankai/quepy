#!/usr/bin/env python
# coding: utf-8

# Copyright (c) 2012, Machinalis S.R.L.
# This file is part of quepy and is distributed under the Modified BSD License.
# You should have received a copy of license in the LICENSE file.
#
# Authors: Rafael Carrascosa <rcarrascosa@machinalis.com>
#          Gonzalo Garcia Berrotaran <ggarcia@machinalis.com>

"""
Tests for Regex module.
"""

import unittest
from quepy.parsing import QuestionTemplate, Particle, Lemma
from quepy.tagger import Word


class Mockrule(object):
    rulename = "Mock"


class TestQuestionTemplate(unittest.TestCase):
    def setUp(self):
        self.mockrule = Mockrule

        class SomeRegex(QuestionTemplate):
            regex = Lemma("hello")

            def interpret(self, match):
                return Mockrule

        class SomeRegexWithData(QuestionTemplate):
            regex = Lemma("hello")

            def interpret(self, match):
                return Mockrule, 42

        self.regexinstance = SomeRegex()
        self.regex_with_data = SomeRegexWithData()

    def test_match(self):
        words = [Word("hi", "hello")]
        ir, userdata = self.regexinstance.get_interpretation(words)
        self.assertTrue(ir is self.mockrule)
        self.assertEqual(userdata, None)

    def test_no_match(self):
        words = [Word("hi", "hello"), Word("girl", "girl")]
        ir, userdata = self.regexinstance.get_interpretation(words)
        self.assertEqual(ir, None)
        self.assertEqual(userdata, None)

    def test_user_data(self):
        words = [Word("hi", "hello")]
        _, userdata = self.regex_with_data.get_interpretation(words)
        self.assertEqual(userdata, 42)

    def test_no_ir(self):
        class SomeRegex(QuestionTemplate):
            regex = Lemma("hello")

        regexinstance = SomeRegex()
        words = [Word("hi", "hello")]
        self.assertRaises(NotImplementedError,
                          regexinstance.get_interpretation, words)

    def test_regex_empty(self):
        class SomeRegex(QuestionTemplate):
            def interpret(self, match):
                return Mockrule, "YES!"

        regexinstance = SomeRegex()
        words = [Word("hi", "hello")]
        ir, userdata = regexinstance.get_interpretation(words)
        self.assertTrue(ir is Mockrule)
        self.assertEqual(userdata, "YES!")

    def test_match_words(self):
        class SomeRegex(QuestionTemplate):
            def interpret(self, match):
                return match

        words = [Word("|@€đ€łł@ð«|µnþ", "hello"), Word("a", "b", "c")]
        match, _ = SomeRegex().get_interpretation(words)
        self.assertEqual(words, match.words)


class TestParticle(unittest.TestCase):
    def setUp(self):
        class Person(Particle):
            regex = Lemma("Jim") | Lemma("Tonny")

            def interpret(self, match):
                return match

        class PersonRegex(QuestionTemplate):
            regex = Person() + Lemma("be") + Person("another")

            def interpret(self, match):
                return match

        class PersonAsset(Person):
            regex = Person() + Lemma("'s") + Lemma("car")

        class NestedParticleRegex(PersonRegex):
            regex = PersonAsset() + Lemma("be") + Person("another")

        self.personregex = PersonRegex()
        self.nestedregex = NestedParticleRegex()

    def test_attrs(self):
        words = [Word(x, x) for x in "Jim be Tonny".split()]
        match, _ = self.personregex.get_interpretation(words)
        self.assertEqual(match.another.words[0], words[-1])
        self.assertEqual(match.person.words[0], words[0])
        self.assertRaises(AttributeError, lambda: match.pirulo)

    def test_nested_particle(self):
        words = [Word(x, x) for x in "Jim 's car be Tonny".split()]
        match, _ = self.nestedregex.get_interpretation(words)
        self.assertEqual(match.personasset.words[0], words[0])
        self.assertRaises(AttributeError, lambda: match.personasset.another)


if __name__ == "__main__":
    unittest.main()
