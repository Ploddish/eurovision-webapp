from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
import jwt
from time import time
from datetime import datetime
from hashlib import md5
import json

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	last_message_read_time = db.Column(db.DateTime)

	user_votes = db.relationship('Vote', backref='voter', lazy='dynamic')
	
	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'],
							algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
			{'reset_password': self.id, 'exp': time() + expires_in},
			app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'],
							algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	song_id = db.Column(db.Integer, db.ForeignKey("song.id"))
	vote_time = db.Column(db.DateTime, default=datetime.utcnow)
	voter_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Song(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True, unique=True)
	artist = db.Column(db.String(64), index=True)
	country = db.Column(db.String(30), index=True, unique=True)
	length = db.Column(db.Integer)
	time_started = db.Column(db.DateTime)

	def __init__(self, country_name, song_artist, song_name, length):
		self.name = song_name
		self.artist = song_artist
		self.country = country_name
		self.length = length