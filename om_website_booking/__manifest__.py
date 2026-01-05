# -*- coding: utf-8 -*-
{
    'name': 'Website Service Booking',
    'version': '18.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Online Service Booking for Customers',
    'description': """
        Website Service Booking Module
        ===============================
        Presentation layer for Service Booking Management System.
        
        Features:
        ---------
        * Public service catalog
        * Online booking form
        * Real-time availability
        * Confirmation page
        * Responsive design
        * Mobile-friendly interface
        
        This module provides the customer-facing website interface.
        Requires om_service_operation for backend logic.
    """,
    'author': 'Truong Hiep',
    'website': '',
    'depends': ['om_service_operation', 'website', 'portal'],
    'data': [
        # Booking Templates (Split for better organization)
        'views/booking/catalog.xml',
        'views/booking/detail.xml',  # Service detail page
        'views/booking/form.xml',
        'views/booking/results.xml',
        # Other Views
        'views/website_menu.xml',
        'views/portal_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'om_website_booking/static/src/css/booking.css',
            'om_website_booking/static/src/js/booking.js',
        ],
    },
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
