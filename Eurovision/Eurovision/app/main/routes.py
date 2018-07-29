from flask import render_template, flash, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required
from app.main import bp
from app.main.forms import EditProfileForm, VoteForm
from app.models import User, Vote, Song
from datetime import datetime
from app import db
import os


def fill_db_with_data():
	songs = [
			Song("Ukraine",			"Mélovin",						"Under the Ladder",	 			179,	"🇺🇦"	),
			Song("Spain",			"Amaia & Alfred",				"Tu Canción",					179,	"🇪🇸"	),
			Song("Slovenia",		"Lea Sirk",						"Hvala ne!",					180,	"🇸🇮"	),
			Song("Lithuania",		"Ieva Zasimauskaité",			"When We're Old",			 	180,	"🇱🇹"	),
			Song("Austria",			"Cesár Sampson",				"Nobody But You",			 	183,	"🇦🇹"	),
			Song("Estonia",			"Elina Nechayeva",				"La forza",		 				184,	"🇪🇪"	),
			Song("Norway",			"Alexander Rybak",				"That's How You Write A Song",	180,	""	),
			Song("Portugal",		"Cláudia Pascoal",				"O jardim",						138,	""	),
			Song("United Kingdom",	"SuRie",						"Storm",						177,	""	),
			Song("Serbia",			"Sanja Ilic & Balkanika",		"Nova Deca",				 	187,	""	),
			Song("Germany",			"Michael Schulte",				"You Let Me Walk Alone",		177,	""	),
			Song("Albania",			"Eugent Bushpepa",				"Mall",		 					187,	""	),
			Song("France",			"Madame Monsieur",				"Mercy",						182,	""	),
			Song("Czech Republic",	"Mikolas Josef",				"Lie To Me",				 	170,	""	),
			Song("Denmark",			"Rasmussen",					"Higher Ground",				183,	""	),
			Song("Australia",		"Jessica Mauboy",				"We Got Love",		 			184,	""	),
			Song("Finland",			"Saara Aalto",					"Monsters",						180,	""	),
			Song("Bulgaria",		"Equinox",						"Bones",						179,	""	),
			Song("Moldova",			"DoReDoS",						"My Lucky Day",				 	182,	""	),
			Song("Sweden",			"Benjamin Ingrosso",			"Dance You Off",			 	180,	""	),
			Song("Hungary",			"AWS",							"Viszlát nyár",					177,	""	),
			Song("Israel",			"Netta",						"Toy",							180,	""	),
			Song("Netherlands",		"Waylon",						"Outlaw in 'Em",			 	176,	""	),
			Song("Ireland",			"Ryan O'Shaughnessy",			"Together",						176,	""	),
			Song("Cyprus",			"Eieni Foureira",				"Fuego",						183,	""	),
			Song("Italy",			"Ermal Meta & Fabrizio Moro",	"Non mi avete fatto niente",	182,	""	)
			]

	for song in songs:
		print("Actually Adding Song ", song.name)
		db.session.add(song)

	db.session.commit()


@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def get_country_flag(country):
	flags = {
		"Ukraine"	: "🇺🇦",
		"Spain"		: "🇪🇸",
		"Slovenia"	: "🇸🇮"
		}

	return flags.get(country, "🏴󠁧󠁢󠁷󠁬󠁳󠁿")

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	
	#fill_db_with_data()

	current_song_index = 20	# where we are in the running order

	all_songs = Song.get_all_songs_before_and_including(current_song_index)

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

@bp.route('/send_message/<song_id>', methods=['GET', 'POST'])
@login_required
def vote(song_to_vote_for):
	user = User.query.filter_by(username=recipient).first_or_404()
	form = MessageForm()
	if form.validate_on_submit():
		msg = Message(author=current_user, recipient=user,
					  body=form.message.data)
		db.session.add(msg)
		user.add_notification('unread_message_count', user.new_messages())
		db.session.commit()
		flash('Your message has been sent.')
		return redirect(url_for('main.user', username=recipient))
	return render_template('send_message.html', title='Send Message',
						   form=form, recipient=recipient)