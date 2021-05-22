import ipaddress
import json

from faker import Factory
from flask import Response

from max_mind.max_mind_model import MaxMindResponse, MaxMindErrorResponse

fake = Factory.create()


def score_handler(request):
    request = json.loads(request.data.decode('utf-8'))
    amount = request.get('order').get('amount')
    region = request.get('billing').get('region')
    ip = request.get('device').get('ip_address')

    r = MaxMindResponse()
    r.risk_score = float(amount)

    if amount == 500:
        return Response(response='INTERNAL SERVER ERROR', status=500)

    if len(region) > 2:
        region_warning = {
            "code": "INPUT_INVALID",
            "warning": "Encountered value at /billing/region that does not meet the required constraints.",
            "input_pointer": "/billing/region"
        }
        setattr(r, 'warnings', [region_warning])

    if ipaddress.ip_address(ip).is_private:
        if ip != '127.0.0.1':
            r = MaxMindErrorResponse()
            r.code = "IP_ADDRESS_RESERVED"
            r.error = f"The IP address '{ip}' is a reserved IP address (private, multicast, etc.)."

    return r
