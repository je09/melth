from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime


db = SQLAlchemy()
ma = Marshmallow()


# DB

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)


class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    description = db.Column(db.String(100))
    final_date = db.Column(db.Date, nullable=False)
    create_date = db.Column(db.Date, default=datetime.now().date())


# Marshmallow Schemas
class DeadlineSchema(ma.Schema):
    class Meta:
        fields = (
            'description', 'final_date'
        )



deadline_schema = DeadlineSchema()
deadlines_schema = DeadlineSchema(many=True)
