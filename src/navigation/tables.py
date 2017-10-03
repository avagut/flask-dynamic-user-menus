"""Build Instruments Related Tables."""

from flask_table import Table, Col, LinkCol, BoolCol, DatetimeCol, DateCol
from flask import url_for


class MenusDetailsTable(Table):
    """Build a menus details table."""

    thead_attrs = {'style': 'font-size:11px'}
    classes = ['table table-striped', 'table table-hover',
               'table table-condensed']

    role_name_id = LinkCol('Edit Details',
                           'navigation.navmenus',
                           url_kwargs=dict(menu='menu_url'),
                           anchor_attrs={'style': 'font-size:12px'})
    menu_name = Col('Menu Name', allow_sort=True,
                    td_html_attrs={'style': 'font-size:12px'})
    menu_text = Col('Menu Details', allow_sort=True,
                    td_html_attrs={'style': 'font-size:12px'})
    menu_url = Col('Menu URL', allow_sort=True,
                   td_html_attrs={'style': 'font-size:12px'})
    is_active = BoolCol('Menu Active', allow_sort=True,
                        td_html_attrs={'style': 'font-size:12px'})
    created_datetime = Col('Menu Created', allow_sort=True,
                           td_html_attrs={'style': 'font-size:12px'})
    last_modified_datetime = Col('Menu Last Modified', allow_sort=True,
                                 td_html_attrs={'style': 'font-size:12px'})
    allow_sort = True

    def sort_url(self, col_key, reverse=False):
        """Process sort url for the columns of the tables."""
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
        return url_for('navigation.navmenus', sort=col_key,
                       direction=direction)
