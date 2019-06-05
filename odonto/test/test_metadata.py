"""
Unittests for odonto.metadata
"""
from django.contrib.auth.models import User
from opal.core.test import OpalTestCase

from odonto import metadata

class PerformerNumberTestCase(OpalTestCase):

    def test_to_dict(self):
        user = User.objects.create(username='no', first_name='Donald', last_name='Harrison')
        user.performernumber_set.create()

        as_dict = metadata.PerformerMetadata.to_dict()

        expected = {
            'performer': {
                'current_user': None,
                'performer_list': ['Donald Harrison']
            }
        }
