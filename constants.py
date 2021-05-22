import random
from enum import Enum


class EventType(Enum):
    APPROVED = ("Approved", 2)
    BAD_ACCOUNT = ("Returned Bad Account", 17)
    CAPTURED = ("Captured", 5)
    COLLECTION_FAILED = ("Collection Failed", 10)
    COLLECTED = ("Collected", 9)
    DECLINED = ("Declined", 1)
    DISPUTED = ("Disputed", 15)
    ORIGINATED = ("Originated", 11)
    PROCESSED = ("Processed", 8)
    PROCESSING_ERROR = ("Processing Error", 3)
    REFUNDED = ("Refunded", 6)
    RETURNED_NSF = ("Returned NSF", 16)
    SENT_TO_COLLECTION = ("Sent To Collection", 14)
    RETURNED_BAD_ACCOUNT = ("Returned Bad Account", 17)
    SETTLED = ("Settled", 12)
    VOIDED = ("Voided", 4)
    UNAUTHORIZED = ("Unauthorized", 21)
    CHARGED_BACK = ("Charged Back", 22)
    NOTICE_OF_CHANGE = ("Notice Of Change", 19)

    def __init__(self, status, tid):
        self.status = status
        self.tid = tid

    def __str__(self):
        return str(self.status)

    def status(self):
        return str(self.status)

    def tid(self):  # enum AchJhEventTypeEnum index
        return str(self.tid)

class Currency(Enum):
    EUR = (978, 2)
    GBP = (826, 2)
    USD = (840, 2)
    JPY = (392, 0)
    BHD = (48, 3)
    JMD = (388, 2)
    AUD = (36, 2)
    CAD = (124, 2)
    MXN = (484, 2)
    DKK = (208, 2)
    KWD = (414, 3)

    def __init__(self, code, minorunits):
        self.code = code
        self.minorunits = minorunits

    @staticmethod
    def rand():
        return random.choice(list(c for c in Currency))

    @staticmethod
    def get_name(code: int):
        return list(filter(lambda field: field.code == code, list(c for c in Currency)))[0].name


class SettlementStatus(Enum):
    CHARGED_BACK = ("Charged Back", 7)
    NO_SETTLEMENT_NEEDED = ("No Settlement Needed", 1)
    PENDING = ("Originated / Settlement Pending", 4)
    SETTLED = ("Settled", 6)
    TO_BE_ORIGINATED = ("To Be Originated", 2)
    ORIGINATING = ("Originating", 3)

    def __init__(self, status, sid):
        self.status = status
        self.sid = sid

    def __str__(self):
        return str(self.status)

    def status(self):
        return str(self.status)

    def sid(self):
        return str(self.sid)


class AchJhTransactionStatus(Enum):
    APPROVED = ("Approved", 2)
    COLLECTED = ("Collected", 6)
    CLOSED_ACCOUNT = ("Invalid / Closed Account", 15)
    DECLINED = ("Declined", 1)
    DISPUTED = ("Disputed", 13)
    ERROR = ("Error", 3)
    IN_COLLECTION = ("In Collection", 10)
    PROCESSED = ("Processed", 5)
    UNCOLLECTED_NSF = ("Uncollected NSF", 14)
    VOIDED = ("Voided", 4)

    def __init__(self, status, tid):
        self.status = status
        self.tid = tid

    def __str__(self):
        return str(self.status)

    def status(self):
        return str(self.status)

    def tid(self):
        return str(self.tid)


class AccountType(Enum):
    CHEQUE = (0, 'CHECKING')
    SAVINGS = (1, 'SAVINGS')

    def __init__(self, code, description):
        self.code = code
        self.description = description

    def code(self):
        return self.code

    def description(self):
        return self.description

    @staticmethod
    def all():
        return list(at.name for at in AccountType)

    @staticmethod
    def rand():
        return random.choice(list(at for at in AccountType))

    @staticmethod
    def find_by_code(code):
        try:
            return list(filter(lambda c: c.code == int(code), list(c for c in AccountType)))[0]
        except IndexError:
            return None
