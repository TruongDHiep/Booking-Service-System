# -*- coding: utf-8 -*-
{
    'name': 'Service Sale Integration',
    'version': '18.0.1.0.0',
    'category': 'Services/Sales',
    'summary': 'Bridge module to integrate Service Appointments with Sales Orders',
    'description': """
        Service Sale Integration
        =========================
        This module extends the Service Booking system with Sales functionality.
        
        Features:
        ---------
        * Generate Sale Orders from confirmed appointments
        * Smart button to view linked quotations
        * Automatic product and pricing integration
        * Prevent duplicate quotation creation
        
        Dependencies:
        -------------
        * om_service_operation (for appointment model)
        * sale_management (for sale order functionality)
    """,
    'author': 'Truong Hiep',
    'website': '',
    'depends': ['om_service_operation', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/appointment_view.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
