import datetime

from serializer import Serializable

NOW = (datetime.datetime.now()).replace(hour=0, minute=0, second=0)
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'


class WSEventReport(Serializable):
    TransactionStatus = None
    TransactionNumber = None
    ReferenceNumber = None
    SettlementStatus = None
    EventDateTime = None
    EventType = None


class GetHistoricalEventReportResponse(Serializable):
    pass


class GetHistoricalEventReportResult(Serializable):
    pass
