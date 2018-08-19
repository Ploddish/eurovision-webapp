from app import db
from app.models import Song

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
		db.session.add(song)		#pylint: disable=E1101

	db.session.commit()			#pylint: disable=E1101

