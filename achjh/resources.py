# coding=utf-8
from flask import make_response
from flask import request
from flask_restful import Resource

from achjh.processing.view import processing
from achjh.reporting.view import reporting


class AchJhReporting(Resource):
    def post(self):
        r = request.data.decode('utf-8')
        headers = {'Content-Type': 'text/xml'}
        response = make_response(reporting(r).__str__().encode(), headers)
        return response


class AchJhProcessing(Resource):
    def post(self):
        r = request.data.decode('utf-8')
        headers = {'Content-Type': 'text/xml'}
        response = make_response(processing(r).__str__().encode(), headers)
        return response
