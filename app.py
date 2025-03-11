from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from forms import *
from models import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '44f6c84390d56356963c706c3ee43059'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/images/'

Bootstrap(app)
csrf = CSRFProtect(app)
db.init_app(app)

@app.route('/')
def book_list():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/book/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_details.html', book=book)

@app.route('/author/<int:author_id>')
def author_details(author_id):
    author = Author.query.get_or_404(author_id)
    books = Book.query.filter_by(author_id=author_id).all()
    return render_template('author_details.html', author=author, books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('book_list'))
    return render_template('form.html', title="Add a New Author", form=form)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    form.author_id.choices = [(author.id, author.name) for author in Author.query.all()]

    if form.validate_on_submit():
        image_filename = 'default.jpg'

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(image_path)
            image_filename = filename

        book = Book(
            name=form.name.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            category=form.category.data,
            author_id=form.author_id.data,
            image=image_filename
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('book_list'))
    return render_template('form.html', title="Add a New Book", form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
