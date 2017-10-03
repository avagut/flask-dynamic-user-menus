"""Contain the views of the users blueprint."""

import datetime
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from src import db, app
from src.users.models import RoleMenu
from src.users.models import Role as rol
from . import models, forms, tables, utils


nav_blueprint = Blueprint('navigation', __name__, template_folder='templates')


@nav_blueprint.route('/')
def index():
    """Set up the homepage."""
    # return 'This is the homepage'
    return redirect(url_for('navigation.list_urls'))

@nav_blueprint.route('/nav/test_menu_roles', methods=['GET', 'POST'])
def menu_roles():
    """Create a list of urls in the app."""
    my_roles = utils.build_auth_menu_roles()
    return str(my_roles)


@nav_blueprint.route('/nav/list_urls', methods=['GET', 'POST'])
def list_urls():
    """Create a list of urls in the app eg for a site map.
       Pending: Create a set comprehension for prepending the base 
       domain to each of the urls."""
    routes = []
    for rule in app.url_map.iter_rules():
        url = rule.rule
        routes.append(url)
    return 'urls in this app are:' + str(set(routes))


@nav_blueprint.route('/nav/menus_management', methods=['GET', 'POST'])
def menus_management():
    """Map menu assignment to roles."""
    role_menus = None
    this_role = None
    is_set_role_menu = None
    roles_form = forms.SelectRoleForm()
    roles_form.role.query = utils.build_active_roles_list()
    role_menu_detail_form = forms.RoleMenuSelectionForm()
    form = forms.NewRoleMenuForm()
    form.role_id.query = utils.build_active_roles_list()
    form.menu_id.query = utils.build_active_menus_list()

    opt_role = request.args.get("role")
    if opt_role:
        role_menus = utils.build_role_menus(opt_role)
        this_role = utils.this_role(opt_role)

    opt_role_menu = request.args.get("ident")
    if opt_role_menu:
        this_role_menu = utils.fetch_this_role_menu(opt_role_menu)
        role_menu_detail_form = forms.RoleMenuSelectionForm(obj=this_role_menu)
        set_role_menu = RoleMenu.query.filter_by(
            role_menu_id=opt_role_menu).first()
        is_set_role_menu = True
        role_menus = utils.build_role_menus(this_role_menu.role_id)

    if request.method == 'POST':
        if form.submit_role_menu and ('role_id' in request.form):
            if form.validate_on_submit():
                menu_id = request.form['menu_id']
                role_id = request.form['role_id']
                if utils.is_currently_rolemenu(role_id, menu_id):
                    flash('Role Menu already exists', 'error')
                    flash_errors(form)
                    return redirect(url_for('navigation.menus_management'))
                role_menu = RoleMenu(
                    menu_id=request.form['menu_id'],
                    role_id=request.form['role_id'],
                    created_by=current_user.user_id
                )
                db.session.add(role_menu)
                db.session.commit()
                utils.build_auth_menu_roles()
                flash('New Role Menu successfully created!', 'success')
                return redirect(url_for('navigation.menus_management'))
            else:
                flash_errors(form)
        if role_menu_detail_form.submit_change_role_menu and \
                ('role_menu_id' in request.form):
            if role_menu_detail_form.validate_on_submit():
                role_menu_detail_form.populate_obj(set_role_menu)
                set_role_menu.modified_by = current_user.user_id
                set_role_menu.last_modified_datetime = datetime.datetime.now()
                db.session.commit()
                utils.build_auth_menu_roles()
                flash('Role menu successfully updated.', 'success')
                return redirect(url_for('navigation.menus_management'))
            else:
                flash_errors(role_menu_detail_form)
    return render_template('menus_management.html', roles_form=roles_form,
                           role_menus=role_menus, this_role=this_role,
                           role_menu_detail_form=role_menu_detail_form,
                           is_set_role_menu=is_set_role_menu, form=form)


@nav_blueprint.route('/nav/menus', methods=['GET', 'POST'])
def navmenus():
    """Process Roles Details.

    Capture role details, display a roles table with a roles search bar.
    """
    searchform = forms.SearchMenuForm()
    sort = request.args.get("sort")
    reverse = (request.args.get('direction', 'asc') == 'desc')
    opt_search = request.args.get("search_string")
    menus_list = utils.build_menus_list(sort, reverse, opt_search)
    menus_table = tables.MenusDetailsTable(menus_list, sort_by=sort,
                                           sort_reverse=reverse)

    opt_menu = request.args.get("menu")
    if opt_menu:
        menu = models.Menu.query.filter_by(menu_url=opt_menu).first()
        form = forms.MenuDetailsForm(obj=menu)
    else:
        form = forms.MenuDetailsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                if opt_menu:
                    form.populate_obj(menu)
                    menu.modified_by = current_user.user_id
                    menu.last_modified_datetime = datetime.now()
                    db.session.commit()
                    flash('Details for menu {} successfully updated.'
                          .format(menu.menu_text), 'success')
                else:
                    menu = models.Menu(
                            menu_name=form.menu_name.data,
                            menu_url=form.menu_url.data,
                            menu_text=form.menu_text.data,
                            created_by=current_user.user_id
                            )
                    db.session.add(menu)
                    db.session.commit()
                    flash('New Menu {} successfully created!'
                          .format(menu.menu_text), 'success')
                return redirect(url_for('navigation.navmenus'))

            except IntegrityError as e:
                flash('Menu already exists', 'error')
                flash_errors(form)
        else:
            flash_errors(form)
    return render_template('menu_details.html', form=form,
                           menus_table=menus_table, searchform=searchform)


def flash_errors(form):
    """Create the form errors array for display in flash message."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                u"Error in the %s field - %s" %
                (getattr(form, field).label.text, error),
                'info')
