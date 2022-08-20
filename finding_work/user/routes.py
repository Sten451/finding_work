
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from finding_work.models import User, db, bcrypt
from finding_work.user.forms import RegistrationForm, LoginForm
from finding_work.config import Config

user = Blueprint('user', __name__)


@user.route("/user/registration", methods=['POST', 'GET'])
def registrations():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit() and form.code.data == Config.KEY_REGISTER:
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    password=hashed_password, user_status=form.user_status.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.authentication'))
    return render_template('registration.html', title='Register', form=form)


@user.route("/user/authentication", methods=['GET', 'POST'])
def authentication():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
    return render_template('authentication.html', title='Аутентификация', form=form)


@user.route("/user/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
