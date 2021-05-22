import json
import pprint

from faker import Factory
from flask import Response, jsonify

from constants import AccountType
from db.db_helpers import DirectDebitHelper, UtilityHelper
from direct_debit.constants import DirectDebitEventType
from direct_debit.models import TransactionSearchItem, Payer, BankAccount
from utils import logger

fake = Factory.create()
db_directdebit = DirectDebitHelper()
db_utility = UtilityHelper()


def login_handler(request, args):
    response = Response()
    user = args.get('Username')
    password = args.get('Password')

    if (user is None or user == '') or (password is None or password == ''):
        response.status_code = 400

    elif user == 'badusername':
        response.status_code = 401

    elif len(password) < 10:
        response = jsonify({
            "errorCode": "BadRequest",
            "errorMessage": "The field Password must be a string with a minimum length of 10 and a maximum length of "
                            "128.",
            "errorDetail": "Password"})
    else:
        response = {
            'access_token': fake.pystr(min_chars=2172, max_chars=2172),
            'expires_in': 3600,
            'token_type': 'Bearer'
        }

    return response


def auth_handler(request, uniqueref):
    request = json.loads(request.data.decode('utf-8'))
    amount = request.get('Amount')
    cents = round(abs(int(amount) - amount), 2)
    if cents == 0.10:
        data = {"errorCode": "InternalServerError", "errorMessage": "An error has occurred, please retry",
                "errorDetail": "Server Error"}
    elif cents == 0.11:
        data = {"errorCode": "BadRequest", "errorMessage": "Date must not be in the past", "errorDetail": "Date"}
    # elif cents == 0.12:  # TODO Unrecognized field "errorCode"
    # (class com.merchant.bank.integrapay.protocol.rest.ScheduleSinglePaymentResponse
    #     data = {"errorCode": "InvalidPayer", "errorMessage": "No payer with UniqueReference of '" + uniqueref + "' was found."}
    else:
        data = {'scheduledPaymentId': str(fake.random_number(7, True))}
    response = jsonify(data)
    return response


def status_update_handler(request, business_id):
    d = []
    all_txns = db_directdebit.direct_debit_open_transactions_list()
    txn_list = list(filter(lambda t: t.responsecode != 'D', all_txns))

    for open_txn in txn_list:
        tx = TransactionSearchItem()
        tx.payer = Payer()
        tx.bankAccount = BankAccount()
        tx_last_event = db_directdebit.get_direct_debit_transaction_last_event(open_txn.id)
        amount = open_txn.amount
        uniqueref = open_txn.uniqueref
        cardholdername = open_txn.cardholdername.split(' ', maxsplit=1)

        tx.business.businessId = business_id
        tx.reference = uniqueref
        tx.description = tx.description.format(amount, uniqueref)
        tx.amount = float(amount)
        tx.amountRequested = float(amount)
        tx.currency = db_utility.get_currency_by_id(open_txn.currency).code

        # payer
        tx.payer.payerId = str(fake.random_number(6, True)) if tx_last_event.payer_id is None else tx_last_event.payer_id
        tx.payer.uniqueReference = uniqueref
        tx.payer.groupReference = uniqueref
        tx.payer.familyOrBusinessName = cardholdername[0]
        tx.payer.familyOrBusinessName = cardholdername[1] if len(cardholdername) == 2 else cardholdername[0]
        tx.payer.givenName = cardholdername[0]
        tx.paymentMethod = tx_last_event.payment_method

        # bankAccount
        tx.bankAccount.accountBranch = tx_last_event.account_branch
        tx.bankAccount.accountNumber = tx_last_event.account_number
        tx.bankAccount.accountName = open_txn.cardholdername
        tx.bankAccount.accountType = AccountType.find_by_code(tx_last_event.account_type).name

        if tx_last_event.status_description == 'NEW':
            cents = abs(round(abs(int(tx.amount) - tx.amount), 2))
            status = DirectDebitEventType.N
            if cents == 0.24:
                status = DirectDebitEventType.P
            elif cents == 0.25:
                status = DirectDebitEventType.C
            elif cents == 0.26:
                status = DirectDebitEventType.R
                status.description = 'Rejected: Not processed (payer inactive)'
                tx.subStatusCode = 'R17'
            elif cents == 0.27:
                status = DirectDebitEventType.L
            elif cents == 0.28:
                status = DirectDebitEventType.LS

            tx.transactionId = str(fake.random_number(7, True))
            tx.statusCode = status.code
            tx.statusDescription = status.description
            d.append(tx)
        elif tx_last_event.status_description == DirectDebitEventType.N.description:
            tx.transactionId = tx_last_event.transaction_id
            tx.statusCode = DirectDebitEventType.SETTLED.code
            tx.statusDescription = DirectDebitEventType.SETTLED.description
            d.append(tx)

    response = jsonify(d)
    logger.warning(20, pprint.pprint(response.json))

    return response
