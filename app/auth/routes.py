from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.models import Users
from app import db
from app.auth.email import send_password_reset_email

from flask_login import login_user, logout_user, current_user
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
import os, shutil
#
#
# @bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     user = Users.query.filter_by(email=form.email.data).first()
#     if user is None or not user.check_password(form.password.data):
#             flash('Wrong email or password')
#             return redirect(url_for('auth.login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('main.index')
#         return redirect(next_page)
#     return render_template('auth/login.html', title='Login', form=form)
#
#
# @bp.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))
#
#
# @bp.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = Users(email=form.email.data)
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         full_path = os.path.join(os.getcwd(), 'app/static', 'profile_files', 'profile_pics')
#         if not os.path.exists(full_path):
#             os.mkdir(full_path)
#         flash('You are new user now!')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/register.html', title='Registration', form=form)
#
#
# @bp.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('main.index'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user = Users.query.filter_by(email=form.email.data).first()
#         if user:
#             send_password_reset_email(user)
#         flash('Check your email for the instructions for reset your password')
#         if current_user.is_authenticated:
#             return redirect(url_for('main.user_page', id=current_user.id))
#         else:
#             return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password_request.html', form=form, title='Reset Password')
#
#
# @bp.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     user = Users.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash('Your password has been reset')
#         if current_user.is_authenticated:
#             return redirect(url_for('main.user_page', id=current_user.id))
#         else:
#             return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password.html', form=form)
#
#
#
#
#
#
#
#
