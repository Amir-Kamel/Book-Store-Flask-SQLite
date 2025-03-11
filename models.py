from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    add_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)