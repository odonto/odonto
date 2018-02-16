from .message import Message

class Patient(Message):
    class Meta:
        schema = {
            # Sex
            #
            # Sex of patient.
            'sex': {
                'type': 'string',
                'allowed': ('M', 'F'),
                'required': True,
            },

            # Date of birth
            #
            # Patient's date of birth.
            'date_of_birth': {
                'type': 'date',
                'required': True,
            },

            # Patient's title
            #
            # (eg. "Mr")
            'title': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 4,
                'required': False,
            },
        }
