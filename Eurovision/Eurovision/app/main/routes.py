from flask import render_template, flash, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required, logout_user
from app.main.forms import EditProfileForm, VoteForm
from app.main import bp
from app.models import User, Vote, Song
from datetime import datetime
from app import db
from app import server_data
from app.helper.database_helpers import fill_db_with_data
import os


@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()		#pylint: disable=E1101
		
		if not server_data.is_user_logged_in(current_user.id):
			server_data.set_user_logged_in(current_user.id)

		if request.endpoint != 'main.room':
			server_data.remove_user_from_any_room(current_user.id)


@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# pick a room
@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	return render_template('index.html', title='Home', rooms=server_data.rooms)

def has_voted_for_song(song_id, voter_id):
	vote_count = Vote.query.filter(Vote.song_id == song_id).\
		filter(Vote.voter_id == voter_id).count()

	return vote_count > 0

def get_all_songs():
	return Song.query.all()

def get_all_songs_before_and_including(song_index=1):
	return Song.query.filter(Song.id <= song_index).all()

@bp.route('/room/<room_name>', methods=['GET', 'POST'])
@login_required
def room(room_name):
	if not server_data.get_room(room_name).is_user_in_room(current_user.id):
		server_data.get_room(room_name).add_user(current_user.id)

	all_songs = get_all_songs_before_and_including(12)

	form = [] #[len(all_songs)]	# dunno if I need all this but eh
	voted_for = [None] * len(all_songs)

	for i, song in enumerate(all_songs):
		form.append(VoteForm(prefix=song.country))

		if form[i].validate_on_submit():
			vote = Vote(form[i].vote.data, song.id, current_user.id)
			print("Adding vote for", song.name, " (id) ", song.id, " for user ", current_user.username, " with value ", form[i].vote.data)

			db.session.add(vote)	#pylint: disable=E1101
			db.session.commit()		#pylint: disable=E1101

		if has_voted_for_song(song.id, current_user.id):
			voted_for[i] = True
		else:
			voted_for[i] = False

	return render_template('room.html', room_name=room_name, title=room_name, form=form, songs=all_songs, voted_for=voted_for)


@bp.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()		#pylint: disable=E1101
		flash('Your changes have been saved.')
		return redirect(url_for('main.user', username=current_user.username))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile',
						   form=form)