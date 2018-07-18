from flask import render_template, flash, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required
from app.main import bp
from app.main.forms import EditProfileForm, VoteForm
from app.models import User, Vote, Song
from datetime import datetime
from app import db
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
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	songs = [
			Song("Ukraine",			"Mélovin",						"Under the Ladder",	 			179	),
			Song("Spain",			"Amaia & Alfred",				"Tu Canción",					179	),
			Song("Slovenia",		"Lea Sirk",						"Hvala ne!",					180	),
			Song("Lithuania",		"Ieva Zasimauskaité",			"When We're Old",			 	180	),
			Song("Austria",			"Cesár Sampson",				"Nobody But You",			 	183	),
			Song("Estonia",			"Elina Nechayeva",				"La forza",		 				184	),
			Song("Norway",			"Alexander Rybak",				"That's How You Write A Song",	180	),
			Song("Portugal",		"Cláudia Pascoal",				"O jardim",						138	),
			Song("United Kingdom",	"SuRie",						"Storm",						177	),
			Song("Serbia",			"Sanja Ilic & Balkanika",		"Nova Deca",				 	187	),
			Song("Germany",			"Michael Schulte",				"You Let Me Walk Alone",		177	),
			Song("Albania",			"Eugent Bushpepa",				"Mall",		 					187	),
			Song("France",			"Madame Monsieur",				"Mercy",						182	),
			Song("Czech Republic",	"Mikolas Josef",				"Lie To Me",				 	170	),
			Song("Denmark",			"Rasmussen",					"Higher Ground",				183	),
			Song("Australia",		"Jessica Mauboy",				"We Got Love",		 			184	),
			Song("Finland",			"Saara Aalto",					"Monsters",						180	),
			Song("Bulgaria",		"Equinox",						"Bones",						179	),
			Song("Moldova",			"DoReDoS",						"My Lucky Day",				 	182	),
			Song("Sweden",			"Benjamin Ingrosso",			"Dance You Off",			 	180	),
			Song("Hungary",			"AWS",							"Viszlát nyár",					177	),
			Song("Israel",			"Netta",						"Toy",							180	),
			Song("Netherlands",		"Waylon",						"Outlaw in 'Em",			 	176	),
			Song("Ireland",			"Ryan O'Shaughnessy",			"Together",						176	),
			Song("Cyprus",			"Eieni Foureira",				"Fuego",						183	),
			Song("Italy",			"Ermal Meta & Fabrizio Moro",	"Non mi avete fatto niente",	182	),
			]


	form = VoteForm()
	return render_template('index.html', title='Home', song_finished=True, form=form, songs=songs, time_left=60)

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