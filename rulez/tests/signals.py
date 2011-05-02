#-*- coding: utf-8 -*-
from django.test.testcases import TestCase
from rulez.rolez.signals import should_we_invalidate_rolez

class MockInstance(object):
    def __init__(self):
        self.called = False
    def rulez_invalidate(self):
        self.called = True

class SignalsTestCase(TestCase):
    def test_handling_forwards_properly(self):
        inst = MockInstance()
        should_we_invalidate_rolez(self, inst)
        self.assertEqual(inst.called, True)