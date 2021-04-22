from flask import Flask
from flask import render_template, redirect
from data import db_session
from data.users import User
from data.products import Product
from forms.user_form import *
from forms.product_form import ProductForm
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    db_sess = db_session.create_session()
    prod = db_sess.query(Product).all()

    return render_template("index.html", prod=prod)


@app.route('/main', methods=["GET", "POST"])
def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    # db_sess.query(User).delete()
    # db_sess.query(Product).delete()
    db_sess.commit()

    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if form.email.data == form.password.data:
            return redirect("/")
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            # jobs = db_sess.query(Jobs).filter(News.is_private == False)
            return render_template('index.html', name=user.name)
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# Работаю здесь --------------------------------------------------------------------------

@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    form = ProductForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Product).filter(User.name == form.name.data).first():
            return render_template('addproduct.html', title='Добавление товара',
                                   form=form,
                                   message="Такой продукт уже есть")
        prod = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data
        )
        db_sess.add(prod)
        db_sess.commit()
        return redirect('/addproduct')
    return render_template('addproduct.html', form=form)


if __name__ == '__main__':
    main()
##