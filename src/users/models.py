"""Contain all user related data structures in models."""

from datetime import datetime
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from src import db, bcrypt


class User(db.Model):
    """Hold User details."""

    __tablename__ = 'sec_users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    user_password = db.Column(db.Binary(60), nullable=False, server_default='')
    roles = db.relationship('Role', secondary='sec_users_roles',
                            backref=db.backref('roles', lazy='dynamic'))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmation_sent_at = db.Column(db.DateTime, nullable=True)
    is_confirmed = db.Column(db.Boolean(), nullable=False,  server_default='0')
    confirmed_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean(), nullable=False, server_default='1')
    is_deleted = db.Column(db.Boolean, server_default='0')
    is_authenticated = db.Column(db.Boolean(), nullable=False, default=False)
    has_ever_logged_in = db.Column(db.Boolean(),
                                   nullable=False, default=False)
    created_datetime = db.Column(db.DateTime, default=datetime.now())
    last_modified_datetime = db.Column(db.DateTime, nullable=True)
    login_datetime = db.Column(db.DateTime, nullable=True)
    password_last_change_datetime = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.Integer)
    modified_by = db.Column(db.Integer)

    def __init__(self, user_name, first_name, last_name, email,
                 is_active, created_by):
        """Set up a new user."""
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = is_active
        self.created_datetime = datetime.now()
        self.confirmation_sent_at = self.created_datetime
        self.created_by = created_by

    @hybrid_property
    def password(self):
        """Return the hash of the password as saved in the database."""
        return self.user_password

    @password.setter
    def set_password(self, plaintext_password):
        """Save the hash for the plaintext password provided by the users."""
        self.user_password = bcrypt.generate_password_hash(plaintext_password)

    def is_correct_password(self, plaintext_password):
        """Check password hash.

        Check if the hash for the plaintext password matches the user hashed
        password.
        """
        return bcrypt.check_password_hash(self.user_password,
                                          plaintext_password)

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return str(self.user_id)

    def is_anonymous(self):
        """Represent an anonymous user, not allowed."""
        return False

    def full_name(self):
        """Build a full name from First Name & Last Name."""
        return self.first_name + ' ' + self.last_name


class Role(db.Model):
    """Hold Role Details."""

    __tablename__ = 'sec_roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False, unique=True)
    role_description = db.Column(db.String(255), nullable=False)
    users = db.relationship('User', secondary='sec_users_roles',
                            backref=db.backref('users', lazy='dynamic'))
    menus = db.relationship('navigation.models.Menu',
                            secondary='nav_roles_menus',
                            backref=db.backref('roles', lazy='dynamic'))
    is_active = db.Column(db.Boolean(), nullable=False, server_default='1')
    created_by = db.Column(db.Integer)
    created_datetime = db.Column(db.DateTime, default=datetime.now())
    modified_by = db.Column(db.Integer)
    last_modified_datetime = db.Column(db.DateTime, nullable=True)
    is_default = db.Column(db.Boolean(), default=False)

    def __init__(self, role_name, role_description,  created_by):
        """Create a new role."""
        self.role_name = role_name
        self.role_description = role_description
        self.created_by = created_by
        self.created_datetime = datetime.now()

    def __repr__(self):
        """Represent an instance of the class."""
        return self.role_name


class UserRole(db.Model):
    """Hold the User Role Details."""

    __tablename__ = 'sec_users_roles'
    user_role_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('sec_users.user_id'),
                        nullable=False, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('sec_roles.role_id'),
                        nullable=False, primary_key=True)
    is_active = db.Column(db.Boolean(), nullable=False, server_default='1')
    created_by = db.Column(db.Integer)
    created_datetime = db.Column(db.DateTime, default=datetime.now())
    modified_by = db.Column(db.Integer)
    last_modified_datetime = db.Column(db.DateTime, nullable=True)
    __table_args__ = (UniqueConstraint('user_role_id',
                                       name='UK_state_user_role'),)

    def __init__(self, user_id, role_id, created_by):
        """Create a new user role."""
        self.role_id = role_id
        self.user_id = user_id
        self.created_by = created_by
        self.created_datetime = datetime.now()


class RoleMenu(db.Model):
    """Hold the Role Menu Details."""

    __tablename__ = 'nav_roles_menus'
    role_menu_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('nav_menus.menu_id'),
                        nullable=False, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('sec_roles.role_id'),
                        nullable=False, primary_key=True)
    can_view = db.Column(db.Boolean(), nullable=False, server_default='True')
    can_create = db.Column(db.Boolean(), nullable=False, server_default='0')
    can_edit = db.Column(db.Boolean(), nullable=False, server_default='0')
    can_delete = db.Column(db.Boolean(), nullable=False, server_default='0')
    is_active = db.Column(db.Boolean(), nullable=False, server_default='True')
    created_by = db.Column(db.Integer)
    created_datetime = db.Column(db.DateTime, default=datetime.now())
    modified_by = db.Column(db.Integer)
    last_modified_datetime = db.Column(db.DateTime, nullable=True)

    def __init__(self, menu_id, role_id, created_by):
        """Create a new role menu combination."""
        self.menu_id = menu_id
        self.role_id = role_id
        self.created_by = created_by
        self.created_datetime = datetime.now()
        self.can_view = True
