from flask_wtf import FlaskForm
from flask_login import login_manager, UserMixin, LoginManager
from wtforms import IntegerField, StringField, TextAreaField, SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    type = StringField('Тип', validators=[DataRequired()])
    price = IntegerField('Цена', validators=[DataRequired()])
    description = TextAreaField('Описание')
    submit = SubmitField('Добавить')