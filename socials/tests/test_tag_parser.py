# -*- coding: utf-8 -*-
from django.test import TestCase

from socials.utils import parse_to_tags


class TagParserTests(TestCase):

    def test_tag_parser_basic(self):
        text = 'test #beauty i am #what '
        tags = parse_to_tags(text)
        self.assertIn('what', tags)
        self.assertIn('beauty', tags)

    def test_tag_parser_starts_with_tag(self):
        text = '#start with tag test #beauty i am #what '
        tags = parse_to_tags(text)
        self.assertIn('start', tags)
        self.assertIn('what', tags)
        self.assertIn('beauty', tags)

    def test_tag_parser_tricky(self):
        text = '#start-,... with tag test i am #what_what #aa-bb #123hop-.- '
        tags = parse_to_tags(text)
        self.assertIn('start', tags)
        self.assertIn('what_what', tags)
        # not yet!
        # self.assertNotIn('123hop', tags)
        # self.assertIn('aa', tags)
