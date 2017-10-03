"""Utility Functions for user module."""

from flask import session
from sqlalchemy import or_, and_
from . import models
from src import db
from src.users.models import Role as rol
from src.users.models import RoleMenu as rol_menu
from . models import Menu as menu


def build_menus_list(sort, reverse, opt_search):
    """Build & display a menus list.

    Display the data sorted by direction and where applicable filtered by
    search string.
    """
    if sort is None:
        sort = 'menu_text'
        reverse = 'asc'
    if reverse:
        reverse = 'desc'
    else:
        reverse = 'asc'
    totalsort = str(str(sort) + ' ' + str(reverse))
    if opt_search is None:
        menus_list = models.Menu.query.order_by(totalsort).all()
    else:
        search_string = '%' + opt_search + '%'
        filter_clause1 = (models.Menu.menu_url.like(search_string))
        filter_clause2 = (models.Menu.menu_text.like(search_string))
        menus_list = models.Menu.query.filter(or_(
            filter_clause1,
            filter_clause2
        )).order_by(totalsort).all()
    return menus_list


def build_roles_list():
    """Build & display a roles list."""
    roles_list = rol.query.order_by(rol.role_name).all()
    return roles_list


def build_active_roles_list():
    """Build & display a roles list."""
    filter_clause1 = rol.is_active == bool(1)
    roles_list = rol.query.filter(filter_clause1).order_by(rol.role_name).all()
    return roles_list


def this_role(role_ids):
    """Build & display a roles list."""
    filter_clause1 = rol.role_id == role_ids
    roled = rol.query.filter(filter_clause1).first()
    return roled.role_name


def build_active_menus_list():
    """Build & display a menus list."""
    filter_clause1 = menu.is_active == bool(1)
    menus_list = menu.query.filter(filter_clause1).order_by(
                                    menu.menu_name).all()
    return menus_list


def build_role_menus(role_name):
    """Build and display a role menu list."""
    role = rol.query.filter_by(role_id=role_name).first()
    filter_clause1 = rol_menu.role_id == role.role_id
    role_menus = db.session.query(rol_menu.role_menu_id, rol.role_id,
                                  rol.role_name,
                                  menu.menu_id, menu.menu_name,
                                  rol_menu.can_view,
                                  rol_menu.can_create, rol_menu.can_edit,
                                  rol_menu.can_delete)\
        .join(rol, rol_menu.role_id == rol.role_id) \
        .join(menu, rol_menu.menu_id == menu.menu_id) \
        .filter(filter_clause1).all()
    return role_menus


def is_currently_rolemenu(role_id, menu_id):
    """Verify if a menu is currently assigned to a role and its active."""
    filter_clause1 = rol_menu.role_id == role_id
    filter_clause2 = rol_menu.menu_id == menu_id
    filter_clause3 = rol_menu.is_active == bool(1)
    return rol_menu.query.filter(and_(
        filter_clause1,
        filter_clause2,
        filter_clause3
    )).first()


def fetch_this_role_menu(opt_role_menu):
    """Fetch the details of one specific role menu."""
    filter_clause1 = rol_menu.role_menu_id == opt_role_menu
    this_role_menu = db.session.query(rol_menu.role_menu_id,
                                      rol_menu.can_view, rol_menu.role_id,
                                      rol_menu.can_create, rol_menu.can_edit,
                                      rol_menu.can_delete,
                                      menu.menu_name) \
        .join(menu, rol_menu.menu_id == menu.menu_id)\
        .filter(filter_clause1).first()
    print(this_role_menu.menu_name)
    return this_role_menu


def build_auth_menu_roles():
    """Build a list of menus and authorized Roles.

    Create a list of the menus and their urls tracked in the Database.
    Fetch the roles authorized to access the menus/urls.
    Create a dictionary and load into the session.
    """
    filter_clause1 = (rol_menu.can_view == bool(1))
    menus_list = db.session.query(rol_menu.menu_id, rol_menu.role_id,
                                  menu.menu_url, rol.role_name) \
        .join(menu, rol_menu.menu_id == menu.menu_id) \
        .join(rol, rol_menu.role_id == rol.role_id) \
        .filter(filter_clause1).all()
    menu_url_list = []
    menu_dict = {}
    for m in menus_list:
        if m.menu_url not in menu_url_list:
            this_url = m.menu_url
            menu_url_list.append(m.menu_url)
    for u in menu_url_list:
        auth_roles = []
        for m in menus_list:
            if m.menu_url == u:
                auth_roles.append(m.role_name)
        menu_dict[u] = auth_roles
    try:
        del session['menu_dict']
    except:
        pass
    session['menu_dict'] = menu_dict
    return menu_dict
