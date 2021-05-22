# coding=utf-8
from flask import Response
from flask import request
from flask_restful import Resource
from flask_restful import reqparse

from direct_debit.controllers import login_handler, status_update_handler, auth_handler


class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Username', type=str)
        parser.add_argument('Password', type=str)
        args = parser.parse_args()
        return login_handler(request, args)


class TransactionSearchList(Resource):
    def get(self, business_id):
        return status_update_handler(request, business_id)

    def post(self, business_id):
        # stub for acknowledge txn status change request
        pass


class Payers(Resource):
    def post(self, business_id):
        pass


class Webhook(Resource):
    def post(self):
        response = Response()
        print(request.args)
        print(request.form)
        print(request.data)
        return response

    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('Username', type=str)
        # parser.add_argument('Password', type=str)
        # args = parser.parse_args(request.args)
        print(request.args)

        # from lxml import etree
        #
        # e = etree.Element('root')
        # e.append(etree.Element("child1"))
        #
        # headers = {'Content-Type': 'text/xml'}
        # response = make_response(etree.tostring(e, pretty_print=True), headers)
        response = Response()
        return response


class BankAccount(Resource):
    def put(self, business_id, uniqueref):
        pass


class Payments(Resource):
    def post(self, business_id, uniqueref):
        return auth_handler(request, uniqueref)
