from datetime import datetime

from faker import Factory

from serializer import Serializable

fake = Factory.create()


class Business(Serializable):
    def __init__(self, business_id='', business_name='GlobalOnePay Test', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.businessId = business_id
        self.businessName = business_name


class Payer(Serializable):
    def __init__(self, uniqueref='', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.payerId = str(fake.random_number(5, True))
        self.uniqueReference = uniqueref
        self.groupReference = uniqueref
        self.familyOrBusinessName = ''
        self.givenName = ''


class BankAccount(Serializable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accountBranch = None
        self.accountNumber = None
        self.accountName = ''
        self.accountType = ''


class TransactionSearchItem(Serializable):
    business = Business()
    time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S:000+00:00')
    transactionId = str(fake.random_number(7, True))
    reference = None
    description = 'ACH Payment made by test for amount {} - [payer unique ref:{}]'
    amount = 0
    amountRequested = 0
    amountRefunded = 0
    currency = None
    type = 'PDB'
    typeDescription = "Payer Debit - Bank Account"
    statusCode = None  # "S",
    statusDescription = None  # "Settled"
    paymentMethod = 'BANKACCOUNT'
    payer = Payer()
    bankAccount = BankAccount()
