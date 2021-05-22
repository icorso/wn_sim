from achjh.achjh_utils import TRANSACTION_DATETIME, wrap
from achjh.reporting.reports.historical_event_report import WSEventReport, GetHistoricalEventReportResponse, \
    GetHistoricalEventReportResult


class AchJhReportingResponse:
    def __init__(self, tn=None, rn=None, events=None):
        self._tn = tn
        self._rn = rn
        self._event = None
        self._events = events if events else []

    @property
    def tn(self):
        return self._tn

    @tn.setter
    def tn(self, value):
        self._tn = value

    @property
    def rn(self):
        return self._rn

    @rn.setter
    def rn(self, value):
        self._rn = value

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, value):
        self._events = value

    def with_event(self, event: WSEventReport):
        if not event.TransactionNumber:
            event.TransactionNumber = self.tn
        if not event.ReferenceNumber:
            event.ReferenceNumber = self.rn
        if not event.TransactionDateTime:
            event.TransactionDateTime = TRANSACTION_DATETIME
        if not event.ReturnCode:
            event.ReturnCode = ""
        event.TotalAmount = 0
        event.OwnerAppReferenceId = 0

        self.events.append(event)
        return self

    def with_rn(self, rn):
        for event in self.events:
            if not event.ReferenceNumber:
                event.ReferenceNumber = rn
        return self

    def with_tn(self, tn):
        for event in self.events:
            if not event.TransactionNumber:
                event.TransactionNumber = tn
        return self

    def __str__(self):
        get_historical_event_report_result = GetHistoricalEventReportResult(WSEventReport=self._events)
        response = GetHistoricalEventReportResponse(GetHistoricalEventReportResult=get_historical_event_report_result)
        r = response.to_xml(pretty_print=True, namespace="https://ssl.selectpayment.com/PV", no_header=True)
        return wrap(r)

    def build(self):
        return self
