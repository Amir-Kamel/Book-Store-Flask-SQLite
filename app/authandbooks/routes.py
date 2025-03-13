from flask import render_template, redirect, url_for, flash, current_app
from app.authandbooks import authandbooks
from app.authandbooks.models import Author, Book
from app.authandbooks.forms import AuthorForm, BookForm
from werkzeug.utils import secure_filename
from app import db
import os


@authandbooks.route('/')
def book_list():
    books = Book.query.all()
    return render_template('books.html', books=books)

@authandbooks.route('/book/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_details.html', book=book)

@authandbooks.route('/author/<int:author_id>')
def author_details(author_id):
    author = Author.query.get_or_404(author_id)
    books = Book.query.filter_by(author_id=author_id).all()
    return render_template('author_details.html', author=author, books=books)


@authandbooks.route('/add_author', methods=['GET', 'POST'])
def add_author():
    form = AuthorForm()

    if form.validate_on_submit():
        # Check if author already exists
        existing_author = Author.query.filter_by(name=form.name.data).first()
        if existing_author:
            flash('Author name already exists! Please choose a different name.', 'danger')
            return redirect(url_for('authandbooks.add_author'))

        author = Author(name=form.name.data)
        author.save()
        flash('Author added successfully!', 'success')
        return redirect(url_for('authandbooks.book_list'))

    return render_template('form.html', title="Add an Author", form=form)

@authandbooks.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    form.author_id.choices = [(author.id, author.name) for author in Author.query.all()]

    if form.validate_on_submit():
        # Check if book name already exists
        existing_book = Book.query.filter_by(name=form.name.data).first()
        if existing_book:
            flash('Book name already exists! Please choose a different name.', 'danger')
            return redirect(url_for('authandbooks.add_book'))

        image_filename = 'default.jpg'

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.root_path, 'static/images', filename)
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
        book.save()
        flash('Book added successfully!', 'success')
        return redirect(url_for('authandbooks.book_list'))

    return render_template('form.html', title="Add a New Book", form=form)


@authandbooks.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    form = BookForm(obj=book)  # Prefill form with existing book data

    # Fix: Populate the author dropdown
    form.author_id.choices = [(author.id, author.name) for author in Author.query.all()]

    # Fix: Set the current book's author
    form.author_id.data = book.author_id

    if form.validate_on_submit():
        book.name = form.name.data
        book.category = form.category.data
        book.price = form.price.data
        book.publish_date = form.publish_date.data
        book.author_id = form.author_id.data  # Now it correctly assigns the author ID

        # Keep old image if no new image is uploaded
        if form.image.data:
            image_filename = form.image.data.filename
            image_path = os.path.join('static/images', image_filename)
            form.image.data.save(image_path)  # Save new image
            book.image = image_filename  # Update book image
        else:
            book.image = book.image  # Keep existing image

        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('authandbooks.book_details', book_id=book.id))

    return render_template('form.html', title="Edit Book", form=form)


@authandbooks.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    static_folder = os.path.join(current_app.root_path, "static", "images")
    if book.image and book.image != "default.jpg":
        image_path = os.path.join(static_folder, book.image)

        if os.path.exists(image_path):
            os.remove(image_path)

    book.delete()
    flash('Book and its image deleted successfully!', 'success')

    return redirect(url_for('authandbooks.book_list'))



@authandbooks.route('/delete_author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get_or_404(author_id)

    static_folder = os.path.join(current_app.root_path, "static", "images")
    for book in author.books:
        if book.image and book.image != "default.jpg":
            image_path = os.path.join(static_folder, book.image)
            if os.path.exists(image_path):
                os.remove(image_path)

    author.delete()

    flash('Author and their books deleted successfully!', 'success')
    return redirect(url_for('authandbooks.book_list'))

@authandbooks.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
