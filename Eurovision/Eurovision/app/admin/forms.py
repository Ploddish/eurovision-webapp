from flask_wtf import FlaskForm
from wtforms.fields.html5 import IntegerRangeField
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Length, NumberRange
from app.models import User

class EditSongForm(FlaskForm):
	id = IntegerField('ID')
	name = StringField('Name')
	artist = StringField('Aritst')
	country = StringField('Country')
	length = IntegerField('Length')
	flag = StringField('Flag')
	delete = SubmitField('Delete')

