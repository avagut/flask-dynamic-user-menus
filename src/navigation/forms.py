"""Contains all the forms for instrument outstanding shares upload."""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,  BooleanField
from wtforms import HiddenField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class MenuDetailsForm(FlaskForm):
    """Form to capture menu details."""

    menu_name = StringField('Menu name', validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    menu_url = StringField('Menu URL', validators=[DataRequired()],
                           render_kw={'class': 'form-control'})
    menu_text = StringField('Menu Details', validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    is_active = SelectField(u'Status',
                            choices=[('True', 'Active'), ('False',
                                                          'Inactive')],
                            validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    submit_menu_details = SubmitField('Save Menu Details',
                                      render_kw={'class': ' btn btn-primary'})


class SearchMenuForm(FlaskForm):
    """Form to search for a menu."""

    search_string = StringField('Menu Detail',  validators=[DataRequired()],
                                render_kw={'class': 'form-control',
                                           "placeholder": "Search Menu"})


class RoleMenuSelectionForm(FlaskForm):
    """Select a menu to add to a role."""

    role_id = QuerySelectField(label=u"Role Name", allow_blank=True,
                               validators=[DataRequired()],
                               render_kw={'class': 'form-control',
                                          'placeholder': "Role Name"})
    menu_id = QuerySelectField(label=u"Menu Name", allow_blank=True,
                               validators=[DataRequired()],
                               render_kw={'class': 'form-control',
                                          'placeholder': "Menu Name"})
    is_active = SelectField(u'Status',
                            choices=[('True', 'Active'),
                                     ('False', 'Inactive')],
                            validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    submit_role_menu = SubmitField('Submit Details',
                                   render_kw={'class': 'btn btn-primary',
                                              "placeholder": "Submit Details"})


class SelectRoleForm(FlaskForm):
    """Select a role to filter menus."""

    role = QuerySelectField(label=u"Role Name", allow_blank=True,
                            validators=[DataRequired()],
                            render_kw={'class': 'form-control',
                                       'placeholder': "Role Name"})
    submit_select_role = SubmitField('Search Role Menus', render_kw={
                                        'class': 'btn btn-success'})


class RoleMenuSelectionForm(FlaskForm):
    """Edit the details of a selected role menu."""

    menu_name = StringField('Role Name', validators=[DataRequired()],
                            render_kw={'class': 'form-control',
                                       'style': 'border:none'})
    can_view = BooleanField(validators=[Optional()],
                            render_kw={'class': 'form-control text-center'})
    can_create = BooleanField(validators=[Optional()],
                              render_kw={'class': 'form-control text-center'})
    can_edit = BooleanField(validators=[Optional()],
                            render_kw={'class': 'form-control text-center'})
    can_delete = BooleanField(validators=[Optional()],
                              render_kw={'class': 'form-control text-center'})
    role_menu_id = HiddenField('Identifier', validators=[DataRequired()],
                               render_kw={'class': 'form-control text-center'})
    submit_change_role_menu = SubmitField('Save Details', render_kw={
                                        'class': 'btn btn-primary'})


class NewRoleMenuForm(FlaskForm):
    """Capture the details of a new Role Menu mapping."""

    role_id = QuerySelectField(label=u"Role Name", allow_blank=True,
                               validators=[DataRequired()],
                               render_kw={'class': 'form-control',
                                          'placeholder': "Role Name"})
    menu_id = QuerySelectField(label=u"Menu Name", allow_blank=True,
                               validators=[DataRequired()],
                               render_kw={'class': 'form-control',
                                          'placeholder': "Menu Name"})
    is_active = SelectField(u'Status',
                            choices=[('True', 'Active'),
                                     ('False', 'Inactive')],
                            validators=[DataRequired()],
                            render_kw={'class': 'form-control'})
    submit_role_menu = SubmitField('Save New Details', render_kw={
                                        'class': 'btn btn-primary'})
