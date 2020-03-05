from datetime import datetime

from flask import jsonify, json

from common import todict


class Result:

    def __init__(self, success=True, result_data=None, message=None):

        self.success = success
        self.data = result_data
        self.message = message

    # def to_json(self):
    #     return {
    #         "success": self.success,
    #
    #         "data": self.data,
    #
    #         "message": self.message
    #     }

    @staticmethod
    def gen_success(data=None, message = None):
        ret = Result(success=True, result_data=data, message=message)

        return jsonify(todict(ret))

    @staticmethod
    def gen_fail(data=None, message=None):
        ret = Result(success=False, result_data=data, message=message)
        return jsonify(todict(ret))
