from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Add Author')

class BookForm(FlaskForm):
    name = StringField('Book Name', validators=[DataRequired(), Length(min=2, max=200)])
    publish_date = DateField("Publish Date", format="%Y-%m-%d", validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=[('under 8', 'Under 8'), ('8-15', '8-15'), ('adults', 'Adults')], validators=[DataRequired()])
    author_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    image = FileField('Book Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')