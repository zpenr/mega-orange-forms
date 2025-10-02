from flask import Blueprint, render_template,request, redirect, abort, flash
from ..extensions import bcrypt, db
from flask_login import login_user, logout_user, current_user
from ..models.user import User
user = Blueprint('user', __name__)

@user.route('/signup', methods = ['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        existing_user = User.query.filter_by(login=request.form['login']).first()
        if existing_user:
            flash('Пользователь с тиким логином уже создан', 'alert')
            return redirect('/signup')
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        if request.form.get('rep-password') == request.form.get('password'):
            user = User(name=request.form['name'], login=request.form['login'], password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегестрированы! Теперь войдите', 'succes')
            return redirect('/login')
        else: 
            flash('Пароли не совпадают!', 'alert')
            return redirect('/signup')
    else:
        if current_user.is_authenticated:
            return render_template("registration/sign-up.html",is_auth = current_user.name)
        else: return render_template("registration/sign-up.html")

@user.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(login=request.form['login']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user, remember=request.form.get('remember'))
            return redirect('/all-forms')
        else: 
            flash("Неверное имя пользователя или пароль", 'alert')
            return redirect('/signup')
    else: return render_template("registration/login.html")
@user.route('/logout', methods = ['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/')