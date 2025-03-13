from app import db
from datetime import datetime


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete-orphan")

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):

        for book in self.books[:]:
            db.session.delete(book)

        db.session.delete(self)
        db.session.commit()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    publish_date = db.Column(db.Date, nullable=False)
    add_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(100), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id', ondelete="CASCADE"), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
