from ..extensions import db
from sqlalchemy.dialects.postgresql import JSON

class Form(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    creator = db.Column(db.String(100))
    description = db.Column(db.String(400))
    time = db.Column(db.String(100))
    questions = db.Column(db.String(300))
    answers_to_questions = db.Column(db.String(100))
    dids = db.Column(JSON)
    scores = db.Column(JSON)