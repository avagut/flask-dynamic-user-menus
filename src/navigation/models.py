"""Contain all navigation related data structures in models."""

from datetime import datetime
from src import db


class Menu(db.Model):
    """Hold Navigation Menu details."""

    __tablename__ = 'nav_menus'
    menu_id = db.Column(db.Integer, primary_key=True)
    menu_url = db.Column(db.String(80), nullable=False, unique=True)
    menu_name = db.Column(db.String(80), nullable=False, unique=True)
    menu_text = db.Column(db.Text, nullable=False)
    menu_roles = db.relationship('users.models.Role',
                                 secondary='nav_roles_menus',
                                 backref=db.backref('menus_roles',
                                                    lazy='dynamic'))
    is_active = db.Column(db.Boolean(), nullable=False, server_default='1')
    created_datetime = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.Integer)
    last_modified_datetime = db.Column(db.DateTime, nullable=True)
    modified_by = db.Column(db.Integer)

    def __init__(self, menu_name, menu_url, menu_text, created_by):
        """Set up a new menu url."""
        self.menu_url = menu_url
        self.menu_name = menu_name
        self.menu_text = menu_text
        self.is_active = True
        self.created_datetime = datetime.now()
        self.confirmation_sent_at = self.created_datetime
        self.created_by = created_by

    def __repr__(self):
        """Represent an instance of the class."""
        return self.menu_name
