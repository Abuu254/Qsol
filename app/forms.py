
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, widgets
from wtforms.widgets import Input
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from markupsafe import Markup
from flask_login import current_user
from wtforms.widgets.core import html_params


# Login form


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

# Regestration form


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # check if username is already in use
    def validate_username(self, username):
        client = User.query.filter_by(username=username.data).first()
        if client is not None:
            raise ValidationError('Username already in use, please use a different username')

    # check if email is already in use
    def validate_email(self, email):
        client = User.query.filter_by(email=email.data).first()
        if client is not None:
            raise ValidationError('Email already in use, please use a different email')

# choosing hospital and department


class hospitalform(FlaskForm):
    hospital = SelectField(u'Hospital', choices=[('None', 'Which Hospital are You Visiting...'), ('Yale Health', 'Yale Health')])
    department = SelectField(u'Department', choices=[('None', 'Which Department are You Visiting...'), ('Inquiry', 'Inquiry'), (
        'Admissions', 'Admissions'), ('Consultation', 'Consultation'), ('Laboratory', 'Laboratory'), ('Pharmacy', 'Pharmacy')])
    submit = SubmitField('Confirm Booking')

# choosing departments


class departments(FlaskForm):
    inquiry = SubmitField('Inquiry')
    admissions = SubmitField('Admissions')
    consultation = SubmitField('Consultation')
    laboratory = SubmitField('Laboratory')
    pharmacy = SubmitField('Pharmacy')

# Admin sign in form


class staff(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# change password form


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_new = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change password')


#  Request Reset password form


class ResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Password Reset Request')


# Reset password form


class ResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# Change username form


class ChangeUsernameForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    username = StringField('New Username', validators=[DataRequired()])
    submit = SubmitField('Change Username')

    def validate_username(self, username):
        client = User.query.filter_by(username=username.data).first()
        if client is not None:
            raise ValidationError('Username already in use, please use a different username')