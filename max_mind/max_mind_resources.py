# coding=utf-8
from flask import request
from flask_restful import Resource

from max_mind.max_mind_controllers import score_handler


class MaxMindScore(Resource):

    def post(self):
        return score_handler(request)
