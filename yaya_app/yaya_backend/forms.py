from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    SubmitField,
    SelectField,
    FileField,
    DateField,
    URLField,
    BooleanField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    URL,
    Optional
)
from flask_wtf.file import FileAllowed


# ==========================================
# ADMIN LOGIN
# ==========================================
class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


# ==========================================
# BRANCH FORM
# ==========================================
class BranchForm(FlaskForm):
    name = StringField(
        "Branch Name",
        validators=[DataRequired(), Length(max=150)]
    )

    location = StringField(
        "Location",
        validators=[Optional(), Length(max=255)]
    )

    pastor = StringField(
        "Pastor",
        validators=[Optional(), Length(max=150)]
    )

    submit = SubmitField("Save Branch")


# ==========================================
# MANUAL UPLOAD
# ==========================================
class ManualUploadForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=200)]
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()]
    )

    file = FileField(
        "Manual File",
        validators=[
            DataRequired(),
            FileAllowed(
                ["pdf", "doc", "docx", "ppt", "pptx"],
                "Only PDF, DOC, DOCX, PPT and PPTX files are allowed."
            )
        ]
    )

    submit = SubmitField("Upload Manual")


# ==========================================
# JOB FORM
# ==========================================
class JobForm(FlaskForm):

    title = StringField(
        "Job Title",
        validators=[DataRequired()]
    )

    company = StringField(
        "Company",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )

    submit = SubmitField("Post Job")


# ==========================================
# ANNOUNCEMENT FORM
# ==========================================
class AnnouncementForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[DataRequired()]
    )

    content = TextAreaField(
        "Content",
        validators=[DataRequired()]
    )

    image = FileField(
        "Image",
        validators=[
            Optional(),
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Images only."
            )
        ]
    )

    video = URLField(
        "Video URL",
        validators=[
            Optional(),
            URL()
        ]
    )

    submit = SubmitField("Publish")


# ==========================================
# EVENT FORM
# ==========================================
class EventForm(FlaskForm):

    title = StringField(
        "Event Title",
        validators=[DataRequired()]
    )

    date = DateField(
        "Event Date",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()]
    )

    submit = SubmitField("Save Event")


# ==========================================
# LIVE STREAM
# ==========================================
class LiveStreamForm(FlaskForm):

    title = StringField(
        "Stream Title",
        validators=[DataRequired()]
    )

    url = URLField(
        "YouTube/Facebook URL",
        validators=[
            DataRequired(),
            URL()
        ]
    )

    submit = SubmitField("Save")


# ==========================================
# CONTACT FORM
# ==========================================
class ContactForm(FlaskForm):

    name = StringField(
        "Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    subject = StringField(
        "Subject",
        validators=[DataRequired()]
    )

    message = TextAreaField(
        "Message",
        validators=[DataRequired()]
    )

    confidential = BooleanField("Confidential")

    submit = SubmitField("Send")