from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, SimpleRegistrationForm, RegistrationForm, \
	ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email
from app import password_for_simple_login
from app import server_data
from datetime import datetime

def login_eurovision_user(user, remember):
	print("Logging in user ", user.username)

	if user is None:
		return

	server_data.set_user_logged_in(user.id)
	if login_user(user, remember=remember):
		print("Successfully logged in user")


@bp.route('/simple_register', methods=['GET', 'POST'])
def simple_register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	
	form = SimpleRegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data.lower(), emoji=form.emoji.data)

		existing_user = User.query.filter_by(username=form.username.data).first()
		if existing_user is not None:
			if server_data.is_user_logged_in(existing_user.id):
				flash("Someone with the username {} already exists! Try another name".format(user.username))
				return render_template('auth/simple_register.html', start_time=server_data.start_time, now=datetime.utcnow(), title='Register', form=form)
			print("User {} already exists, so we're going to log them in.".format(existing_user.username))
			login_eurovision_user(existing_user, remember=True)
			return redirect(url_for('main.index'))
		
		db.session.add(user)		#pylint: disable=E1101
		db.session.commit()			#pylint: disable=E1101
		current_app.logger.info("New user {} has been added!".format(user.username))
		flash('Welcome to the party, {}!'.format(user.username))

		login_eurovision_user(user, remember=True)

		return redirect(url_for('main.index'))
	return render_template('auth/simple_register.html', start_time=server_data.start_time, now=datetime.utcnow(), title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('auth.login'))
		login_eurovision_user(user, remember=form.remember_me.data)
		current_app.logger.info("{} has logged in.".format(user.username))
		return redirect(url_for('main.index'))
	return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
	server_data.set_user_logged_out(current_user.id)
	logout_user()
	return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)

		if User.query.filter_by(username=form.username.data).first() is not None:
			flash("Someone with the username {} already exists! Try another name".format(user.username))
			return render_template('auth/register.html', title='Register', form=form)

		user.set_password(form.password.data)
		db.session.add(user)		#pylint: disable=E1101
		db.session.commit()			#pylint: disable=E1101
		current_app.logger.info("New user {} has been added!".format(user.username))
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', title='Register', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	form = ResetPasswordRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_password_reset_email(user)
		flash('Check your email for the instructions to reset your password')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password_request.html',
						   title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.index'))
	user = User.verify_reset_password_token(token)
	if not user:
		return redirect(url_for('main.index'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.set_password(form.password.data)
		db.session.commit()		#pylint: disable=E1101
		flash('Your password has been reset.')
		return redirect(url_for('auth.login'))
	return render_template('auth/reset_password.html', form=form)
