from flask import render_template, flash, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required
from app.main.forms import EditProfileForm, VoteForm
from app.main import bp
from app.models import User, Vote, Song
from datetime import datetime
from app import db
from app.helper.database_helpers import fill_db_with_data
import os


@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@bp.route('/', methods=['GET', 'POST'])
def landling():
	return render_template('landing.html', title='Welcome')

@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	all_songs = Song.get_all_songs_before_and_including(0)

	form = [] #[len(all_songs)]	# dunno if I need all this but eh
	voted_for = [None] * len(all_songs)

	for i, song in enumerate(all_songs):
		form.append(VoteForm(prefix=song.country))

		if form[i].validate_on_submit():
			vote = Vote(form[i].vote.data, song.id, current_user.id)
			print("Adding vote for", song.name, " (id) ", song.id, " for user ", current_user.username, " with value ", form[i].vote.data)

			db.session.add(vote)
			db.session.commit()

		if Vote.has_voted_for_song(song.id, current_user.id):
			voted_for[i] = True
		else:
			voted_for[i] = False

	return render_template('index.html', title='Home', form=form, songs=all_songs, voted_for=voted_for)

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
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('main.user', username=current_user.username))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Edit Profile',
						   form=form)