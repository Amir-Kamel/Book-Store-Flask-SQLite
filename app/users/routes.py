from flask import render_template, redirect, url_for, flash, request
from sqlalchemy.sql.functions import current_user
from flask_login import login_user, logout_user, login_required, current_user
from app.users import users
from app.users.models import User
from app.users.forms import LoginForm, RegistrationForm


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('users.login'))

        new_user = User(
            username=form.username.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)

        new_user.save()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('users.login'))

    return render_template("auth_form.html", title="Register", form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # If already logged in, redirect
        return redirect(url_for('authandbooks.book_list'))

    form = LoginForm()
    next_page = request.args.get('next')

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('authandbooks.book_list'))
        flash('Invalid credentials', 'danger')
    return render_template("auth_form.html", title="Login", form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('users.login'))

@users.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404