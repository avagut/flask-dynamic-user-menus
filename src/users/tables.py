"""Build Instruments Related Tables."""

from flask_table import Table, Col, LinkCol, BoolCol, DatetimeCol, DateCol
from flask import url_for


class UserDetailsTable(Table):
    """Build a users details table."""

    thead_attrs = {'style': 'font-size:11px'}
    classes = ['table table-striped',
               'table table-hover', 'table table-condensed']

    user_name_id = LinkCol('Edit Details', 'users.users_processing',
                           url_kwargs=dict(user_name='user_name'),
                           anchor_attrs={'style': 'font-size:12px'})
    user_name = Col('User Name', allow_sort=True,
                    td_html_attrs={'style': 'font-size:12px'})
    full_name = Col('Employee Name', allow_sort=False,
                    td_html_attrs={'style': 'font-size:12px'})
    email = Col('Email', allow_sort=True,
                td_html_attrs={'style': 'font-size:12px'})
    confirmation_sent_at = Col('Confirmed Date', allow_sort=True,
                               td_html_attrs={'style': 'font-size:12px'})
    is_confirmed = BoolCol('Confirmed Email', allow_sort=True,
                           td_html_attrs={'style': 'font-size:12px'})
    confirmed_at = Col('Confirmed Date', allow_sort=True,
                       td_html_attrs={'style': 'font-size:12px'})
    is_active = BoolCol('User Active', allow_sort=True,
                        td_html_attrs={'style': 'font-size:12px'})
    created_datetime = Col('User Created', allow_sort=True,
                           td_html_attrs={'style': 'font-size:12px'})
    login_datetime = Col('Last Logged In', allow_sort=True,
                         td_html_attrs={'style': 'font-size:12px'})
    password_last_change_datetime = \
        Col('Last Password Change',
            allow_sort=True, td_html_attrs={'style': 'font-size:12px'})
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        """Process sort url for the columns of the tables."""
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('users.users_processing',
                       sort=col_key, direction=direction)


class RolesDetailsTable(Table):
    """Build a role details table."""

    thead_attrs = {'style': 'font-size:11px'}
    classes = ['table table-striped', 'table table-hover',
               'table table-condensed']

    role_name_id = LinkCol('Edit Details', 'users.roles_processing',
                           url_kwargs=dict(role_name='role_name'),
                           anchor_attrs={'style': 'font-size:12px'})
    role_name = Col('Role Name', allow_sort=True,
                    td_html_attrs={'style': 'font-size:12px'})
    role_description = Col('Role Description', allow_sort=False,
                           td_html_attrs={'style': 'font-size:12px'})
    is_active = BoolCol('Role Active', allow_sort=True,
                        td_html_attrs={'style': 'font-size:12px'})
    created_datetime = Col('Role Created', allow_sort=True,
                           td_html_attrs={'style': 'font-size:12px'})
    last_modified_datetime = Col('Role Modified', allow_sort=True,
                                 td_html_attrs={'style': 'font-size:12px'})
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        """Process sort url for the columns of the tables."""
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('users.users_processing', sort=col_key,
                       direction=direction)


class UserRolesTable(Table):
    """Build a user roles details table."""

    thead_attrs = {'style': 'font-size:11px'}
    classes = ['table table-striped',
               'table table-hover', 'table table-condensed']

    role_name_id = LinkCol('Unassign Role', 'users.user_processing',
                           url_kwargs=dict(role_name='role_name'),
                           anchor_attrs={'style': 'font-size:12px'})
    role_name = Col('Role Name', allow_sort=True,
                    td_html_attrs={'style': 'font-size:12px'})
    role_description = Col('Role Description', allow_sort=False,
                           td_html_attrs={'style': 'font-size:12px'})
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        """Process sort url for the columns of the tables."""
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('users.users_processing', sort=col_key,
                       direction=direction)
