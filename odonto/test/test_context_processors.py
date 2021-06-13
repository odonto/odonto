"""
Unittests for odonto.context_processors
"""
from django.contrib.auth.models import AnonymousUser, User
from opal.core.test import OpalTestCase

from odonto import context_processors as cp


class OdontoRolesTestCase(OpalTestCase):

    def test_false_by_default(self):
        request = self.rf.get('/')
        request.user = AnonymousUser()

        ctx = cp.odonto_roles(request)

        self.assertEqual(False, ctx['roles']['is_dentist'])
        self.assertEqual(False, ctx['roles']['is_admin'])

    def test_user_without_performer_number(self):
        request = self.rf.get('/')
        request.user = User.objects.create(username='no')

        ctx = cp.odonto_roles(request)

        self.assertEqual(False, ctx['roles']['is_dentist'])
        self.assertEqual(True, ctx['roles']['is_admin'])

    def test_user_with_performer_number(self):
        request = self.rf.get('/')
        user = User.objects.create(username='no')
        user.performernumber_set.create()
        request.user = user

        ctx = cp.odonto_roles(request)

        self.assertEqual(True, ctx['roles']['is_dentist'])
        self.assertEqual(True, ctx['roles']['is_admin'])

    def test_custom_role(self):
        request = self.rf.get('/')
        user = User.objects.create(username='no')
        user.profile.roles.create(name="something")
        request.user = user
        ctx = cp.odonto_roles(request)
        self.assertTrue(ctx['roles']['something'])
