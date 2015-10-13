# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from permission.tests.utils import create_user
from permission.tests.utils import create_bridge
from permission.tests.utils import create_article
from permission.utils.field_lookup import field_lookup


class PermissionUtilsFieldLookupTestCase(TestCase):
    def setUp(self):
        self.author = create_user('permission_test_articles_author')
        self.editor1 = create_user(
            'permission_test_articles_editor1')
        self.editor2 = create_user(
            'permission_test_articles_editor2')
        self.bridge1 = create_bridge()
        self.bridge2 = create_bridge()
        self.bridge3 = create_bridge()
        self.model = create_article('permission_test_article',
                                    self.author, self.bridge1)
        self.model.editors.add(self.editor1)
        self.model.editors.add(self.editor2)
        self.model.multiple_bridge.add(self.bridge2)
        self.model.multiple_bridge.add(self.bridge3)

    def test_field_lookup_author(self):
        field_value = field_lookup(self.model, 'author')
        self.assertEqual(field_value, self.author)

    def test_field_lookup_author_username(self):
        field_value = field_lookup(self.model, 'author__username')
        self.assertEqual(field_value, self.author.username)

    def test_field_lookup_editors(self):
        field_value = field_lookup(self.model, 'editors')
        field_value = (x for x in field_value.iterator())
        expected_value = map(repr, (self.editor1, self.editor2))
        self.assertQuerysetEqual(field_value, expected_value)

    def test_field_lookup_editors_username(self):
        field_value = list(field_lookup(self.model, 'editors__username'))
        expected_value = [x.username for x in
                          (self.editor1, self.editor2)]
        self.assertEqual(field_value, expected_value)

    def test_field_lookup_single_bridge_author(self):
        field_value = field_lookup(self.model, 'single_bridge__author')
        self.assertEqual(field_value, self.bridge1.author)

    def test_field_lookup_single_bridge_author_username(self):
        field_value = field_lookup(self.model,
                                   'single_bridge__author__username')
        self.assertEqual(field_value, self.bridge1.author.username)

    def test_field_lookup_single_bridge_editors(self):
        field_value = field_lookup(self.model, 'single_bridge__editors')
        field_value = (x for x in field_value.iterator())
        expected_value = list(map(repr, self.bridge1.editors.iterator()))
        self.assertQuerysetEqual(field_value, expected_value)

    def test_field_lookup_single_bridge_editors_username(self):
        field_value = list(field_lookup(self.model,
                                        'single_bridge__editors__username'))
        expected_value = [x.username for x in self.bridge1.editors.iterator()]
        self.assertEqual(field_value, expected_value)

    def test_field_lookup_multiple_bridge_author(self):
        field_value = field_lookup(self.model, 'multiple_bridge__author')
        expected_value = list(map(repr, (self.bridge2.author,
                                         self.bridge3.author)))
        self.assertQuerysetEqual(field_value, expected_value)

    def test_field_lookup_multiple_bridge_author_username(self):
        field_value = field_lookup(self.model,
                                   'multiple_bridge__author__username')
        field_value = list(field_value)
        expected_value = [x.username for x in (self.bridge2.author,
                                               self.bridge3.author)]
        self.assertEqual(field_value, expected_value)

    def test_field_lookup_multiple_bridge_editors(self):
        field_value = list(field_lookup(self.model,
                                        'multiple_bridge__editors'))
        field_value = [
            [repr(x) for x in field_value[0].iterator()],
            [repr(x) for x in field_value[1].iterator()],
        ]
        expected_value1 = [repr(x) for x in self.bridge2.editors.iterator()]
        expected_value2 = [repr(x) for x in self.bridge3.editors.iterator()]
        expected_value = [expected_value1, expected_value2]
        self.assertEqual(field_value, expected_value)

    def test_field_lookup_multiple_bridge_editors__name(self):
        field_value = field_lookup(self.model,
                                   'multiple_bridge__editors__username')
        field_value = list(map(list, field_value))
        expected_value1 = [x.username for x in self.bridge2.editors.iterator()]
        expected_value2 = [x.username for x in self.bridge3.editors.iterator()]
        expected_value = [expected_value1, expected_value2]
        self.assertEqual(field_value, expected_value)

