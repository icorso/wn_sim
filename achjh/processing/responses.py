from serializer import Serializable
from achjh.achjh_utils import wrap


class BaseResponse(Serializable):
    def __str__(self):
        response = self.to_xml(pretty_print=True, namespace="https://ssl.selectpayment.com/PV", no_header=True)
        return wrap(response)


class BaseTransactionResult(BaseResponse):
        ReferenceNumber = None
        Success = None
        Error = None
        ResponseCode = None
        ActualDate = None
        OriginatedAs = None


class AuthorizeTransactionResponse(BaseResponse):
    AuthorizeTransactionResult = BaseTransactionResult


class VoidTransactionResponse(BaseResponse):
    VoidTransactionResult = BaseTransactionResult


class RefundTransactionResponse(BaseResponse):
    RefundTransactionResult = BaseTransactionResult
