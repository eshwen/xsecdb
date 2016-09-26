from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField, DateField

from wtforms import validators, ValidationError


class DeleteForm(Form):

    object_id = TextField("Object ID", [validators.DataRequired("Please enter the Object ID")])
#    updateKey = TextField("Update Key", [validators.DataRequired()])
    submit = SubmitField("Delete Document")
