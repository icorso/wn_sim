from sqlalchemy import and_

from db.db_models import OpenTransaction, ClosedTransaction, AchjhTransaction, AchjhTransactionStateHistory
from db.mysql_client import DbSession
from utils import logger

db = DbSession()


class AchJhTransactionsHelper(object):
    def __init__(self, terminal_id=None):
        self._terminal_id = terminal_id

    def find_no_events_transactions(self):
        tx_list = []
        txs_filter = [OpenTransaction.responsecode != 'D', OpenTransaction.cardtype == 26]
        if self._terminal_id:
            txs_filter.append(OpenTransaction.terminalid == self._terminal_id)

        for tx in db.query_all(OpenTransaction, and_(*txs_filter)):
            if len(self.find_transaction_events(tx.id)) == 0:
                tx_list.append(tx)

        for t in tx_list:  # exclude parent refund tx_list
            opened_tx = list(filter(lambda OpenTransaction: OpenTransaction.id == t.originaltransactionid, tx_list))
            if t.originaltransactionid and len(opened_tx) > 0:
                tx_list.remove(opened_tx[0])

        logger.warning(self.__class__.__name__ + '/' + db.db + ' - \'' + str(len(tx_list))
                       + '\' transactions without events collected.')
        return tx_list

    def find_transaction(self, tx_id):
        tx = db.query_first(OpenTransaction, OpenTransaction.id == tx_id)
        if tx is None:
            tx = db.query_first(ClosedTransaction, ClosedTransaction.id == tx_id)
        return tx

    def find_gray_area_transactions(self):
        txs = []
        for t in db.query_all(ClosedTransaction, ClosedTransaction.amount.contains('.90')):
            if db.query_first(AchjhTransaction, and_(AchjhTransaction.gray_area == 0, AchjhTransaction.id == t.id)):
                txs.append(t)
        logger.warning(self.__class__.__name__ + '/' + db.db + ' - \'' + str(len(txs))
                       + '\' of gray area transaction(s) found.')
        return txs

    def find_refunded_originals(self):
        txs = []
        for t in db.query_all(OpenTransaction, OpenTransaction.originaltransactionid != None):
            if self.is_ach_transaction(t.id):
                txs.append(self.find_transaction(t.originaltransactionid))
        return txs

    def is_transaction_closed(self, tx_id):
        return db.query_first(ClosedTransaction, ClosedTransaction.id == tx_id)

    def is_ach_transaction(self, tx_id):
        return db.query_first(AchjhTransaction, AchjhTransaction.id == tx_id)

    def find_transaction_events(self, tx_id):
        return db.query_all(AchjhTransactionStateHistory, AchjhTransactionStateHistory.transaction_id == tx_id)
