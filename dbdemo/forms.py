from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class MyForm(FlaskForm):
    name = StringField(label = "Name", validators = [DataRequired(message = "Name is a required field.")])

    surname = StringField(label = "Surname", validators = [DataRequired(message = "Surname is a required field.")])

    email = StringField(label = "Email", validators = [DataRequired(message = "Email is a required field."), Email(message = "Invalid email format.")])

    submit = SubmitField("Create")

class FieldForm(FlaskForm):
    field=StringField(label="Επιστημονικο πεδιο:",validators=[DataRequired(message = "Το επιστημονικο πεδιο ειναι απαραιτητο")])
    
    submit = SubmitField("ΥΠΟΒΟΛΗ ΑΙΤΗΜΑΤΟΣ")

class Field3(FlaskForm):
    date = StringField(label="Ημερομηνια")
    duration = StringField(label="Διαρκεια σε χρονια")
    staff = StringField(label="Στελεχος χειριστη")
    submit = SubmitField("ΥΠΟΒΟΛΗ")

class ProjectForm(FlaskForm):
    field=StringField(label="Project title:",validators=[DataRequired(message = "Το ονομα του εργου ειναι απαραιτητο")])
    
    submit = SubmitField("ΥΠΟΒΟΛΗ ΑΙΤΗΜΑΤΟΣ")