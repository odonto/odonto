from django.contrib.auth.models import User
from opal.core.test import OpalTestCase
from odonto.management.commands import create_test_users


class TestCreateUserTestCase(OpalTestCase):
    def test_command(self):
        cmd = create_test_users.Command()
        cmd.handle()
        usernames = [
            'super', 'dentist', 'nurse'
        ]
        self.assertEqual(
            User.objects.filter(username__in=usernames).count(),
            3
        )
