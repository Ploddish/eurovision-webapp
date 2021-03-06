from flask_wtf import FlaskForm
from wtforms.fields.html5 import IntegerRangeField
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length, NumberRange
from app.models import User

class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	emoji = StringField('Emoji', validators=[DataRequired(), Length(min=1, max=5)])
	#sound = SelectField('Sound', )
	submit = SubmitField('Submit')

	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username

	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			if user is not None:
				raise ValidationError('Please use a different username.')

class VoteForm(FlaskForm):
	vote = IntegerRangeField('test', default=6)
	submit = SubmitField('Vote!')