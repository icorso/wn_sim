from enum import Enum


class DirectDebitEventType(Enum):
    SETTLED = ("Settled", 12)
    N = ("Not Submitted", 23)
    P = ("Pending", 24)
    C = ("Cleared", 25)
    R = ("Rejected", 26)
    L = ("Late Rejected", 27)
    LS = ("Late Rejected Settled", 28)

    def __init__(self, description, code):
        self.description = description
        self.code = code

    def code(self):
        return self.code

    def description(self):
        return self.description
