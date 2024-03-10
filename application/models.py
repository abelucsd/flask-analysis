from . import db
from sqlalchemy.dialects.postgresql import JSON

class SampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    json_data = db.Column(JSON)    