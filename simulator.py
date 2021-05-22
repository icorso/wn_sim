from flask import Flask
from flask_restful import Api

from achjh.resources import AchJhProcessing, AchJhReporting
from direct_debit.resources import Login, TransactionSearchList, Payers, BankAccount, Payments, Webhook
from max_mind.max_mind_resources import MaxMindScore

app = Flask(__name__)
api = Api(app)

# ACH IntegraPay simulator endpoints
api.add_resource(Login, '/login')
api.add_resource(TransactionSearchList, '/businesses/<int:business_id>/transactions/new')
api.add_resource(Payers, '/businesses/<int:business_id>/payers')
api.add_resource(BankAccount, '/businesses/<int:business_id>/payers/<string:uniqueref>/accounts/bank-account')
api.add_resource(Payments, '/businesses/<int:business_id>/payers/<string:uniqueref>/schedules/payments')
api.add_resource(Webhook, '/webhook')

# ACH JH simulator endpoints
api.add_resource(AchJhProcessing, '/achjh/processing')
api.add_resource(AchJhReporting, '/achjh/reporting')

# MaxMind v.2 endpoints
api.add_resource(MaxMindScore, '/minfraud/v2.0/score')

if __name__ == "__main__":
    # app.run(ssl_context='adhoc', debug=False, port=8001)
    app.run(debug=False, host='127.0.0.1', port=8001)
