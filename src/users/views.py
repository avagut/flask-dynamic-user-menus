"""Contain the views of the market indices blueprint."""
import datetime
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import render_template, Blueprint, request, \
                    redirect, url_for, flash, session
from flask_login import logout_user, login_user, current_user, login_required
from itsdangerous import URLSafeTimedSerializer, BadSignature
from src import app, db
from src.navigation.utils import build_auth_menu_roles
from . import models, forms, utils, tables
from .utils import has_required_roles


users_blueprint = Blueprint('users', __name__, template_folder='templates',
                            static_folder='static')


@users_blueprint.route('/unauthorized', methods=['GET'])
@login_required
def unauthorized_access():
    """Error Handling page to inform user of unauthorized access."""
    return 'unauthorized access'

#################################################################
# Example Usage:                                                #
@users_blueprint.route('/test', methods=['GET', 'POST'])        #       
@login_required                                                 #
@has_required_roles('users.testview')                           #
def testview():                                                 #
    """Test the required roles process."""                      #
    return str(build_auth_menu_roles())                         #
                                                                #
#################################################################

@users_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def base_page():
    """Redirect the homepage access to the login page."""
    print('is auth is {}'.format(current_user.is_authenticated))
    if current_user.is_authenticated:
        return redirect(url_for('users.index'))
    else:
        return redirect(url_for('users.login'))


@users_blueprint.route('/forgottenpassword', methods=['GET', 'POST'])
def forgottenpassword():
    """Commence a request to reset a password for a user."""
    form = forms.EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User.query.filter_by(email=form.email.data).first()
            if user and user.is_confirmed:
                full_name = user.first_name + ' ' + user.last_name
                utils.send_forgotten_password_email(full_name, user.email)
                msg1 = 'Password change request sent to {} '.format(user.email)
                msg2 = 'successfully, check for email!'
                flash(msg1+msg2, 'success')
                return redirect(url_for('users.login'))
            else:
                msg1 = 'Email entered doesnt match any confirmed email address'
                flash(msg1, 'error')
        else:
            flash_errors(form)
    return render_template('forgotten_email.html', form=form)


@users_blueprint.route('/users/reconfirm', methods=['GET', 'POST'])
def reconfirm_email():
    """Commence a request to reset a password for a user."""
    form = forms.EmailForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User.query.filter_by(email=form.email.data).first()
            if user:
                full_name = user.first_name + ' ' + user.last_name
                login_url = url_for('users.login')
                username = user.user_name
                utils.send_confirmation_email(full_name, user.email,
                                              login_url, username)
                flash('Email confirmation request sent to {} successfully, '
                      'check for email!'
                      .format(user.email), 'success')
                return redirect(url_for('users.login'))
            else:
                flash('Email entered doesnt match any confirmed email '
                      'address', 'error')
        else:
            flash_errors(form)
    return render_template('forgotten_email.html', form=form)


@users_blueprint.route('/passwordreset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """Process a user token to reset password.

    Receive a token sent through email and verify that its valid and not
    yet timed out.
    Redirect to a change password page to allow user to create a password
    with email locked.
    """
    try:
        forgotten_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = forgotten_serializer.loads(token,
                                           salt='forgotten-password-salt',
                                           max_age=app.config['TOKEN_TIMEOUT'])
    except BadSignature:
        flash('The password request link is invalid or has expired. Contact '
              'your system admin', 'error')
        return redirect(url_for('users.login'))

    user = models.User.query.filter_by(email=email).first()
    if user.is_confirmed:
        form = forms.ChangePasswordForm(email=email)
        if request.method == 'POST':
            if form.validate_on_submit():
                user.password = form.password.data
                user.password_last_change_datetime = datetime.now()
                db.session.add(user)
                db.session.commit()
                flash('Password changed successfully.', 'success')
                return redirect(url_for('users.login'))
            else:
                flash_errors(form)
        return render_template('password_change.html', form=form)


@users_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def index():
    """Landing Page for users after login."""
    return 'this is the dashboard'


@users_blueprint.route('/users', methods=['GET', 'POST'])
@login_required
def users_processing():
    """Process User Details.

    Capture & edit user details, display a users table with a users search bar.
    Assign & unassign a role to a user after verifying that the role wasn't
     already assigned.
    """
    searchform = forms.SearchUserForm()
    sort = request.args.get("sort")
    reverse = (request.args.get('direction', 'asc') == 'desc')
    opt_search = request.args.get("search_string")
    users_list = utils.build_users_list(sort, reverse, opt_search)
    users_table = tables.UserDetailsTable(users_list, sort_by=sort,
                                          sort_reverse=reverse)
    assign_form = forms.AssignRoleForm()
    user_roles_list = None
    show_roles = "hidden"
    if request.is_xhr:  # Ajax calls
        my_action = request.form['my_action']
        if my_action == 'unassign_role':
            role_name = request.form['role_name']
            user_name = request.form['user_name']
            return utils.unassign_user_role(role_name, user_name)

    opt_user = request.args.get("user_name")
    if opt_user:
        user = models.User.query.filter_by(user_name=opt_user).first()
        form = forms.UserDetailsForm(obj=user)
        user_roles_list = utils.fetch_user_role_list(user)
        show_roles = ''
    else:
        form = forms.UserDetailsForm()
    role_list = utils.fetch_role_list()
    assign_form.role.query = role_list
    if request.method == 'POST':
        print(request.form)
        if assign_form.submit_assign.data:
            if assign_form.validate_on_submit():
                try:
                    """db.session.rollback()#Temporary rollback"""
                    user_name = assign_form.role_user_name.data
                    role_id = assign_form.role.data.role_id
                    user = models.User.query.filter_by(
                        user_name=user_name).first()
                    my_user_role = utils.is_currently_assigned(role_id,
                                                               user.user_id)
                    if my_user_role:
                        msg1 = 'User already assigned to selected role'
                        flash(msg1, 'error')
                        flash_errors(assign_form)
                        return redirect(url_for('users.users_processing',
                                                user_name=user_name))
                    user_role = (models.UserRole(
                        user_id=user.user_id,
                        role_id=role_id,
                        created_by=current_user.user_id
                    ))
                    db.session.add(user_role)
                    db.session.commit()
                    msg1 = 'User {0} successfully added to the {1} Role.' \
                        .format(user.user_name,
                                assign_form.role.data.role_name)
                    flash(msg1, 'success')
                    return redirect(url_for('users.users_processing',
                                            user_name=user_name))
                except IntegrityError as e:
                    db.session.rollback()
                    flash('User already assigned to selected role', 'error')
                    flash_errors(assign_form)
            else:
                flash_errors(assign_form)

        if form.submit_user_details.data:
            if form.validate_on_submit():
                try:
                    if opt_user:
                        form.populate_obj(user)
                        user_name = user.user_name
                        user.modified_by = current_user.user_id
                        user.last_modified_datetime = datetime.now()
                        db.session.commit()
                        flash('Details for user {} successfully updated.'
                              .format(user.user_name), 'success')
                        return redirect(url_for('users.users_processing'))
                    else:
                        user = models.User(
                                user_name=form.user_name.data,
                                first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data,
                                is_active=form.is_active.data,
                                created_by=current_user.user_id
                                )
                        db.session.add(user)
                        db.session.commit()
                        full_name = user.first_name + ' ' + user.last_name
                        login_url = url_for('users.login')
                        username = user.user_name
                        user_name = user.user_name
                        utils.send_confirmation_email(full_name, user.email,
                                                      login_url, username)
                        msg1 = 'User {} successfully created! Advise user'\
                            .format(user.user_name)
                        msg2 = ' to confirm their email address.'
                        flash(msg1+msg2, 'success')
                    return redirect(url_for('users.users_processing',
                                            user_name=user_name))

                except IntegrityError as e:
                    flash('UserName/Email already exists', 'error')
                    flash_errors(form)
            else:
                flash_errors(form)
    return render_template('user_details.html', form=form,
                           users_table=users_table, searchform=searchform,
                           assign_form=assign_form,
                           user_roles_list=user_roles_list,
                           show_roles=show_roles)


@users_blueprint.route('/users/roles', methods=['GET', 'POST'])
@login_required
def roles_processing():
    """Process Roles Details.

    Capture role details, display a roles table with a roles search bar.
    """
    searchform = forms.SearchRoleForm()
    sort = request.args.get("sort")
    reverse = (request.args.get('direction', 'asc') == 'desc')
    opt_search = request.args.get("search_string")
    roles_list = utils.build_roles_list(sort, reverse, opt_search)
    roles_table = tables.RolesDetailsTable(roles_list, sort_by=sort,
                                           sort_reverse=reverse)

    opt_role = request.args.get("role_name")
    if opt_role:
        role = models.Role.query.filter_by(role_name=opt_role).first()
        form = forms.RoleDetailsForm(obj=role)
    else:
        form = forms.RoleDetailsForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                if opt_role:
                    form.populate_obj(role)
                    role.modified_by = current_user.user_id
                    role.last_modified_datetime = datetime.now()
                    db.session.commit()
                    flash('Details for role {} successfully updated.'
                          .format(role.role_name), 'success')
                else:
                    role = models.Role(
                            role_name=form.role_name.data,
                            role_description=form.role_description.data,
                            created_by=current_user.user_id
                            )
                    db.session.add(role)
                    db.session.commit()
                    flash('New Role {} successfully created!'
                          .format(role.role_name), 'success')
                return redirect(url_for('users.roles_processing'))

            except IntegrityError as e:
                flash('Role already exists', 'error')
                flash_errors(form)
        else:
            flash_errors(form)
    return render_template('role_details.html', form=form,
                           roles_table=roles_table, searchform=searchform)


@users_blueprint.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    """Process a user token to confirm email address.

    Receive a token sent through email and verify that its valid
    and not  yet timed out.
    Redirect to a change password page to allow user to create
    a password with email locked.
    """
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt',
                                         max_age=app.config['TOKEN_TIMEOUT'])
    except BadSignature:
        msg1 = 'The confirmation link is invalid or has expired.'
        msg2 = ' Contact your system admin'
        flash(msg1+msg2, 'error')
        return redirect(url_for('users.login'))

    user = models.User.query.filter_by(email=email).first()
    if user.is_confirmed:
        flash('Account already confirmed. Please login.', 'info')
        logout_user()
        return redirect(url_for('users.login'))
    else:
        form = forms.ChangePasswordForm(email=email)
        if request.method == 'POST':
            if form.validate_on_submit():
                user.password = form.password.data
                user.is_confirmed = True
                user.has_ever_logged_in = True
                user.confirmed_at = datetime.now()
                user.password_last_change_datetime = datetime.now()
                db.session.add(user)
                db.session.commit()
                flash('Password changed successfully.', 'success')
                return redirect(url_for('users.login'))
            else:
                flash_errors(form)
        return render_template('password_change.html', form=form)


@users_blueprint.route('/users/login', methods=["GET", "POST"])
def login():
    """Log in user to the system.

    Pass a username and plaintext password and return a boolean value of state.
    """
    form = forms.UsernamePasswordForm()
    if request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            user = models.User.query.filter_by(
                    user_name=form.username.data).first()
            if user and user.is_correct_password(form.password.data):
                user.is_authenticated = True
                user.login_datetime = datetime.now()
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                build_auth_menu_roles()
                return redirect(url_for('users.index'))
            else:
                print('invalid form')
                flash('Wrong UserName or Password.', 'error')
                return redirect(url_for('users.login'))
        else:

            flash_errors(form)
    return render_template('login.html', form=form)


@users_blueprint.route('/users/logout')
@login_required
def logout():
    """Log out currently logged in user.

    Requires no parameters but user must be logged in.
    """
    logout_user()
    return redirect(url_for('users.login'))


def flash_errors(form):
    """Create the form errors array for display in flash message."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                u"Error in the %s field - %s" %
                (getattr(form, field).label.text, error),
                'info')
