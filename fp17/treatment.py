from .utils import min_digits, max_digits
from .message import Message


class Treatment(Message):
    """
    Repeating treatment type (used in tst and cur segments).
    """

    class Meta:
        schema = {
            # Treatment code
            #
            'code': {
                'type': 'number',
                'min': min_digits(4),
                'max': max_digits(4),
                'required': True,
            },

            # Number of instances
            #
            # The number of times the treatment code occurs in the
            # course of treatment.
            'instance_count': {
                'type': 'number',
                'min': min_digits(0),
                'max': max_digits(2),
                'required': True,
            },

            # Tooth identification code
            #
            'teeth': {
                'type': 'list',
                'schema': {
                    'type': 'string',
                    'regex': '^[1-8][1-9]$',
                    'required': True,
                },
                'required': True,
                'minlength': 0,
                'maxlength': 36,
            },

        }
