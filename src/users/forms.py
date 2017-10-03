"""Contains all the forms for instrument outstanding shares upload."""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired, Email, length, EqualTo, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class EmailForm(FlaskForm):
    """Form to capture user email."""

    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={'class': 'form-control',
                                   "placeholder": "User Email"})


class UserDetailsForm(FlaskForm):
    """Form to capture user details."""

    user_name = StringField('User Name', validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    first_name = StringField('First Name', validators=[DataRequired()],
                             render_kw={'class': 'form-control'})
    last_name = StringField('Last Name', validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={'class': 'form-control'})
    is_active = SelectField(u'Status',
                            choices=[('True', 'Active'), ('False',
                                                          'Inactive')],
                            validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    submit_user_details = SubmitField('Save Details',
                                      render_kw={'class': ' btn btn-primary'})


class AssignRoleForm(FlaskForm):
    """Form to specify new assigned role."""

    role_user_name = HiddenField('User Name', validators=[DataRequired()],
                                 render_kw={'class': 'form-control'})
    role = QuerySelectField(label=u"Available Roles", allow_blank=False,
                            validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    submit_assign = SubmitField('Assign This Role',
                                render_kw={'class': ' btn btn-success'})


class ChangePasswordForm(FlaskForm):
    """Form to capture password details."""

    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={'class': 'form-control', 'readonly': True})
    password = PasswordField('New Password',
                             validators=[DataRequired(),
                                         EqualTo('confirm',
                                         message='Passwords must match'),
                                         length(min=6, max=20)],
                             render_kw={'class': 'form-control'})
    confirm = PasswordField('Repeat Password',
                            render_kw={'class': 'form-control'})


class UsernamePasswordForm(FlaskForm):
    """Form to capture user password combo."""

    username = StringField('User name',  validators=[DataRequired()],
                           render_kw={'class': 'form-control',
                                      "placeholder": "User Name"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={'class': 'form-control',
                                        "placeholder": "Password"})
    remember_me = BooleanField(default=False, validators=[Optional()])


class SearchUserForm(FlaskForm):
    """Form to search for a user."""

    search_string = StringField('User Detail',  validators=[DataRequired()],
                                render_kw={'class': 'form-control',
                                           "placeholder": "Search User"})


class SearchRoleForm(FlaskForm):
    """Form to search for a role."""

    search_string = StringField('Role Detail',  validators=[DataRequired()],
                                render_kw={'class': 'form-control',
                                           "placeholder": "Search Role"})


class RoleDetailsForm(FlaskForm):
    """Form to capture role details."""

    role_name = StringField('Role Name', validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    role_description = StringField('Role Description',
                                   validators=[DataRequired()],
                                   render_kw={'class': 'form-control'})
    is_active = SelectField(u'Status',
                            choices=[('True', 'Active'), ('False',
                                                          'Inactive')],
                            validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
