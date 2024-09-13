import json

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()
class User(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    user_id = db.Column(db.Integer,unique =True,nullable = False)
    api_calls = db.Column(db.Integer,default=1)
    logs = db.Column(db.DateTime,default = datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(100))
    paragraph = db.Column(db.Text,nullable = False)
    embedding = db.Column(db.Text,nullable = False)
    logs = db.Column(db.DateTime,dafault = datetime.utcnow)

    def save_embed(self,embedding):
        self.embedding = json.dumps(embedding)

    def get_embed(self):
        return json.loads(self.embedding)
