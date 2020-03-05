import datetime
from decimal import Decimal
from bson import ObjectId
from flask import json


def todict(obj, classkey=None):

    # print("todict of {}".format(obj))
    if isinstance(obj, (int, str)):
        return obj
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")

    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data

    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "_data") and isinstance(obj._data, dict):

        data = {}
        for (k, v) in obj._data.items():
            data[k] = todict(v, classkey)
        return data

    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):

        # print("obj has __dict__")
        data = dict([(key, todict(value, classkey))
                     for key, value in obj.__dict__.items()

                     if not key.startswith('_')
                     ])

        # if not callable(value) and not key.startswith('_') and key not in ['name']

        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__

        # print("__dict__ return:{}".format(data))
        return data

    else:
        # print("no action return:{}".format(obj))
        return obj


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):

        # print("-----------JSONEncoder:{}".format(type(obj)))
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        if hasattr(obj, 'to_json'):
            return obj.to_json()

        # return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

        return json.JSONEncoder.default(self, obj)