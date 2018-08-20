from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
import jwt
from time import time
from datetime import datetime
from hashlib import md5
import json

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)						#pylint: disable=E1101
	username = db.Column(db.String(64), index=True, unique=True)		#pylint: disable=E1101
	email = db.Column(db.String(120), index=True, unique=True)			#pylint: disable=E1101
	password_hash = db.Column(db.String(128))							#pylint: disable=E1101
	about_me = db.Column(db.String(140))								#pylint: disable=E1101
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)			#pylint: disable=E1101
	emoji = db.Column(db.String(10))									#pylint: disable=E1101

	user_votes = db.relationship('Vote', backref='voter', lazy='dynamic')	#pylint: disable=E1101
	
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

@login.user_loader
def load_user(id):
	if not id.isdigit():
		print("HELP!")
		return User.query.first()

	return User.query.get(int(id))

class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)					#pylint: disable=E1101
	vote_value = db.Column(db.Integer)								#pylint: disable=E1101
	song_id = db.Column(db.Integer, db.ForeignKey("song.id"))		#pylint: disable=E1101
	vote_time = db.Column(db.DateTime, default=datetime.utcnow)		#pylint: disable=E1101
	voter_id = db.Column(db.Integer, db.ForeignKey("user.id"))		#pylint: disable=E1101
	
	def __repr__(self):
		return '<Vote {}>'.format(self.id)

	def __init__(self, value, song_id, voter_id):
		self.vote_value = value
		self.song_id = song_id
		self.voter_id = voter_id

class Song(db.Model):
	id = db.Column(db.Integer, primary_key=True)					#pylint: disable=E1101
	name = db.Column(db.String(64), index=True, unique=True)		#pylint: disable=E1101
	artist = db.Column(db.String(64), index=True)					#pylint: disable=E1101
	country = db.Column(db.String(30), index=True, unique=True)		#pylint: disable=E1101
	length = db.Column(db.Integer)									#pylint: disable=E1101
	time_started = db.Column(db.DateTime)							#pylint: disable=E1101
	country_flag = db.Column(db.String(10))							#pylint: disable=E1101
	
	#def get_all_songs_voted_for(self, user):

	
	def __repr__(self):
		return '<Song {}>'.format(self.name)

	def __init__(self, country_name, song_artist, song_name, length, flag):
		self.name = song_name
		self.artist = song_artist
		self.country = country_name
		self.length = length
		self.country_flag = flag