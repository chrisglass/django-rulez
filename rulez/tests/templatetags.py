#-*- coding: utf-8 -*-

from django.test.testcases import TestCase
from django.contrib.auth.models import AnonymousUser, User
from django.template import Template, Context, TemplateSyntaxError

from rulez import registry
from rulez.tests.backend import MockUser


class MockModel(object):
    pk = 999

    def mock_positive_permission(self, user):
        return True

    def mock_negative_permission(self, user):
        return False


class TemplatetagTestCase(TestCase):

    def create_fixtures(self):
        self.user = MockUser()
        self.inactive_user = MockUser(is_active=False)
        self.model = MockModel()

    def render_template(self, template, context):
        context = Context(context)
        return Template(template).render(context)

    def assertYesHeCan(self, permission, user):
        registry.register(permission, MockModel)
        rendered = self.render_template(
            "{% load rulez_perms %}"
            "{% rulez_perms " + permission + " object as can %}"
            "{% if can %}yes he can{% else %}no can do{% endif %}",
            {
                "user": user,
                "object": MockModel()
            }
        )
        self.assertEqual(rendered, "yes he can")

    def assertNoHeCant(self, permission, user):
        registry.register(permission, MockModel)
        rendered = self.render_template(
            "{% load rulez_perms %}"
            "{% rulez_perms " + permission + " object as can %}"
            "{% if can %}yes he can{% else %}no he can't{% endif %}",
            {
                "user": user,
                "object": MockModel()
            }
        )
        self.assertEqual(rendered, "no he can't")

    def test_active_user_against_positive_permission(self):
        self.assertYesHeCan("mock_positive_permission", User(is_active=True))

    def test_active_user_for_negative_permission(self):
        self.assertNoHeCant("mock_negative_permission", User(is_active=True))

    def test_inactive_user_against_positive_permission(self):
        self.assertNoHeCant("mock_positive_permission", User(is_active=False))

    def test_inactive_user_against_negative_permission(self):
        self.assertNoHeCant("mock_negative_permission", User(is_active=False))

    def test_anonymous_user_against_positive_permission(self):
        self.assertYesHeCan("mock_positive_permission", AnonymousUser())

    def test_anonymous_user_against_negative_permission(self):
        self.assertNoHeCant("mock_negative_permission", AnonymousUser())

    def test_active_user_against_missing_permission(self):
        permission = "missing"
        rendered = self.render_template(
            "{% load rulez_perms %}"
            "{% rulez_perms " + permission + " object as can %}"
            "{% if can %}yes he can{% else %}no he can't{% endif %}",
            {
                "user": User(is_active=True),
                "object": MockModel()
            }
        )
        self.assertEqual(rendered, "no he can't")

    def test_invalid_user(self):
        self.assertRaisesRegexp((TemplateSyntaxError, AttributeError),
            "'NoneType' object has no attribute 'has_perm'",
            self.render_template,
            "{% load rulez_perms %}{% rulez_perms mock_positive_permission object as can %}", {
                "object": MockModel(), "user": None
            })

    def test_tag_syntax(self):
        registry.register("mock_positive_permission", MockModel)

        # TODO: error messages from template tag a bit are confusing.
        self.assertRaisesRegexp(TemplateSyntaxError, "tag requires exactly three arguments", self.render_template,
            "{% load rulez_perms %}{% rulez_perms mock_positive_permission object %}", {})

        self.assertRaisesRegexp(TemplateSyntaxError, "tag requires exactly three arguments", self.render_template,
            "{% load rulez_perms %}{% rulez_perms mock_positive_permission object can %}", {})

        self.assertRaisesRegexp(TemplateSyntaxError, "third argument to tag must be 'as'", self.render_template,
            "{% load rulez_perms %}{% rulez_perms mock_positive_permission object can can %}", {})
