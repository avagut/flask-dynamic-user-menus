"""Utility Functions for user module."""

import functools
from flask import render_template, url_for, jsonify, session, redirect
from flask_login import current_user
from flask_mail import Message

from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import or_, and_
from src import app, mail, db
from src.navigation.utils import build_auth_menu_roles
from . import models
from .models import Role as rol
from .models import UserRole as usr_rol


def send_async_email(msg):
    """Send generic email using threaded approach."""
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, html_body):
    """Create Generic Email for dispatch."""
    msg = Message(subject, recipients)
    msg.html = html_body
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()


def send_confirmation_email(full_name, user_email, login_url, username):
    """Send Confirmation Email for user registration."""
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    confirm_url = url_for(
        'users.confirm_email',
        token=confirm_serializer.dumps(user_email,
                                       salt='email-confirmation-salt'),
        _external=True)
    html = render_template(
        'email_confirmation.html',
        confirm_url=confirm_url,
        name=full_name,
        login_url=login_url,
        username=username
        )
    send_email('Confirm Your Email Address', [user_email], html)


def send_forgotten_password_email(user_name, user_email):
    """Send Email Request for user forgotten password."""
    forgotten_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    forgotten_url = url_for(
        'users.password_reset',
        token=forgotten_serializer.dumps(user_email,
                                         salt='forgotten-password-salt'),
        _external=True)
    html = render_template(
        'email_forgotten_password.html',
        forgotten_url=forgotten_url, user_name=user_name)
    send_email('Forgotten Password Reset', [user_email], html)


def build_users_list(sort, reverse, opt_search):
    """Build & display a user list.

    Display the data sorted by direction and where applicable filtered by
     search string.
    """
    if sort is None:
        sort = 'user_name'
        reverse = 'asc'
    if reverse:
        reverse = 'desc'
    else:
        reverse = 'asc'
    totalsort = str(str(sort) + ' ' + str(reverse))
    if opt_search is None:
        users_list = models.User.query.order_by(totalsort).all()
    else:
        search_string = '%' + opt_search + '%'
        filter_clause1 = (models.User.user_name.like(search_string))
        filter_clause2 = (models.User.first_name.like(search_string))
        filter_clause3 = (models.User.last_name.like(search_string))
        filter_clause4 = (models.User.email.like(search_string))
        users_list = models.User.query.filter(or_(
            filter_clause1,
            filter_clause2,
            filter_clause3,
            filter_clause4
        )).order_by(totalsort).all()
    return users_list


def fetch_role_list():
    """Build up the role list."""
    filter_clause1 = rol.is_active == bool(1)
    filter_clause2 = rol.is_default == bool(0)
    return rol.query.filter(and_(
        filter_clause1,
        filter_clause2
    )).order_by(rol.role_name).all()


def fetch_user_role_list(user):
    """Build up the user roles list."""
    filter_clause1 = usr_rol.user_id == user.user_id
    filter_clause2 = usr_rol.is_active == bool(1)
    user_role_list = db.session.query(rol.role_name,
                                      rol.role_description)\
        .join(usr_rol, usr_rol.role_id == rol.role_id) \
        .filter(and_(
            filter_clause1,
            filter_clause2)).all()
    return user_role_list


def build_roles_list(sort, reverse, opt_search):
    """Build & display a roles list.

    Display the data sorted by direction and where applicable filtered by
     search string.
    """
    if sort is None:
        sort = 'role_name'
        reverse = 'asc'
    if reverse:
        reverse = 'desc'
    else:
        reverse = 'asc'
    totalsort = str(str(sort) + ' ' + str(reverse))
    if opt_search is None:
        roles_list = models.Role.query.order_by(totalsort).all()
    else:
        search_string = '%' + opt_search + '%'
        filter_clause1 = (models.Role.role_description.like(search_string))
        filter_clause2 = (models.Role.role_name.like(search_string))
        roles_list = models.Role.query.filter(or_(
            filter_clause1,
            filter_clause2
        )).order_by(totalsort).all()
    return roles_list


def unassign_user_role(role_name, user_name):
    """Unassign a role from a user."""
    user = models.User.query.filter_by(user_name=user_name).first()
    role = models.Role.query.filter_by(role_name=role_name).first()

    filter_clause1 = models.UserRole.role_id == role.role_id
    filter_clause2 = models.UserRole.user_id == user.user_id
    for r in models.UserRole.query.filter(and_(
        filter_clause1,
        filter_clause2
    )).all():
        r.is_active = False
    db.session.commit()
    return jsonify(errorstate=0)


def is_currently_assigned(role_id, user_id):
    """Verify if a role is currently assigned to a user and its active."""
    filter_clause1 = models.UserRole.role_id == role_id
    filter_clause2 = models.UserRole.user_id == user_id
    filter_clause3 = models.UserRole.is_active == bool(1)
    return models.UserRole.query.filter(and_(
        filter_clause1,
        filter_clause2,
        filter_clause3
    )).first()


def fetch_current_user_roles():
    """Get the roles that the current user is assigned to."""
    current_user_roles = list(current_user.roles)
    if current_user_roles:
        current_user_roles = [str(r) for r in current_user_roles]
        return current_user_roles


def fetch_url_roles(view_function):
    """Fetch the roles of the selected url."""
    my_url = url_for(view_function)
    if session is None:
        build_auth_menu_roles()
    return session['menu_dict'][my_url]


def has_required_roles(view_function):
    """Validate whether current user in the authorized role.

    Create a decorator function to fetch current user roles.
    Fetch the authorized roles for the url passed in the parameter.
    If the user roles are not in the authorized list, redirect to
    unauthorized page.
    """
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user:
                return redirect(url_for('users.login'))
            user_roles = fetch_current_user_roles()
            url_roles = fetch_url_roles(view_function)
            print(user_roles, url_roles)
            print(session['menu_dict'])
            auth = any(i in url_roles for i in user_roles)
            if not auth:
                return redirect(url_for('users.unauthorized_access'))
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator
