from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ManualUploadForm(FlaskForm):
    title = StringField('Manual Title', validators=[DataRequired()])
    
    description = TextAreaField('Description', validators=[DataRequired()])
    
    category = SelectField('Category', choices=[
        ('Fellowship', 'Fellowship'),
        ('Policy', 'Policy'),
        ('General', 'General')
    ], validators=[DataRequired()])
    
    icon_class = StringField('FontAwesome Icon (e.g., fa-bible)', validators=[DataRequired()])
    
    # This handles the actual PDF file
    file = FileField('Upload PDF', validators=[
        FileRequired(),
        FileAllowed(['pdf'], 'PDFs only!')
    ])
    
    submit = SubmitField('Upload Manual')