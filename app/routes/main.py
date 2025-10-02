from flask import Blueprint, render_template, redirect
from flask_login import login_user, logout_user, current_user

main = Blueprint('main', __name__)
@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('main/main.html',is_auth = current_user.name)
    else: return render_template('main/main.html')