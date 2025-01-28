from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Create/edit messages form."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Add new user form."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class EditProfileForm(FlaskForm):
    """Edit profile form."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Header Image URL')
    location = StringField('Location')
    bio = TextAreaField('Bio')
    password = PasswordField('Password', validators=[Length(min=6)])


class ChangePasswordForm(FlaskForm):
    """Change password form."""

    curr_password = PasswordField('Current Password', validators=[Length(min=6)])
    new_password_init = PasswordField('New Password', validators=[Length(min=6)])
    new_password_confirm = PasswordField('New Password', validators=[Length(min=6)])