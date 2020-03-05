
from mongo import db


class User(db.Document):
    uid = db.IntField(required=True)
    name = db.StringField(required=True, max_length=100)
    email = db.StringField(max_length=200)
    password = db.StringField(requied=True, min_length=6)
    createtime = db.DateTimeField(required=True)

    # def to_json(self):
    #     return {
    #         "uid": self.uid,
    #         "name": self.name,
    #         "email": self.email
    #     }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.uid)


