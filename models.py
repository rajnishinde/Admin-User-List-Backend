from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer,nullable=True, primary_key=True)
    fname = db.Column(db.String(200), nullable=True)
    lname = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(300),nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

   