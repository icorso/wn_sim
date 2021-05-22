from faker import Factory

from serializer import Serializable

fake = Factory.create()


class MaxMindResponse(Serializable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = fake.uuid4()
        self.risk_score = None   # will be set as amount value of the request field
        self.funds_remaining = float(fake.pydecimal(left_digits=2, right_digits=2, positive=True))
        self.queries_remaining = fake.pyint()
        self.ip_address = {"risk": 0.01}


class MaxMindErrorResponse(Serializable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.code = None
        self.error = None
