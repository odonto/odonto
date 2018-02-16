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
        }
