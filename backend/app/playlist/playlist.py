from mongo import db

import mongoengine_goodjson as gj


class Playlist(gj.Document):
    uid = db.IntField(required=True)
    name = db.StringField(required=True, max_length=100)
    create_time = db.DateTimeField(required=True)
    items = db.ListField(required=False)

    # def to_json(self):
    #     return {
    #         "uid": self.uid,
    #         "name": self.name,
    #         "create_time": self.create_time
    #     }
