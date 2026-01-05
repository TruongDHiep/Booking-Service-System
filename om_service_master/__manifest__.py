# -*- coding: utf-8 -*-
{
    'name': 'Service Master Data',
    'version': '18.0.1.0.0',
    'category': 'Services',
    'summary': 'Master Data Management for Service Booking System',
    'description': """
        Service Master Data Module
        ===========================
        Foundation layer for Service Booking Management System.
        
        Features:
        ---------
        * Manage service master data
        * Service catalog with pricing
        * Service duration configuration
        * Image gallery for services
        
        This module provides the core data structures without business logic.
        Install om_service_operation for booking operations.
    """,
    'author': 'Truong Hiep',
    'website': '',
    'depends': ['base', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/booking_service_views.xml',
        'views/menu_views.xml',
    ],
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
