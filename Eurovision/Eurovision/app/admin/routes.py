from flask import render_template, request
from flask_login import login_required
from app.admin import bp
from app.models import Song
from app.admin.forms import EditSongForm

@login_required
@bp.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('admin/home.html')

@login_required
@bp.route('/songs', methods=['GET', 'POST'])
def songs():
	if request.method == 'GET':
		forms = []
		songs = Song.query.all()

		for song in songs:
			form = EditSongForm()
			form.id.data = song.id
			form.name.data = song.name
			form.artist.data = song.artist
			form.country.data = song.country
			form.length.data = song.length
			form.flag.data = song.country_flag
			forms.append(form)

		return render_template('admin/songs.html', songs=songs, forms=forms)