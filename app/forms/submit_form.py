from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class SubmitForm(FlaskForm):
  search = StringField('Search', validators=[DataRequired()])
