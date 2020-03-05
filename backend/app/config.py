import logging


class Config(object):
    # ...
    MONGO_URI = 'mongodb://localhost:27070/freeiptv'

    # MONGO_URI = 'mongodb://freeiptv.cn:27070/freeiptv'
    MONGO_DBNAME = 'freeiptv'

    THUMB_WORKDER_COUNT = 10

    LOGGING_LEVEL = logging.DEBUG