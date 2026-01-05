# -*- coding: utf-8 -*-
{
    "name": "Service Operations",
    "version": "18.0.1.0.0",
    "category": "Services",
    "summary": "Service Booking Operations and Workflow Management",
    "description": """
        Service Operations Module
        ==========================
        Business logic layer for Service Booking Management System.
        
        Features:
        ---------
        * Appointment booking management
        * Booking state workflow (Draft → Confirmed → Done/Cancel)
        * Automatic overlap checking
        * Calendar and Kanban views
        * Email notifications via Chatter
        * Activity management
        
        This module handles all booking business logic.
        Requires om_service_master for master data.
    """,
    "author": "Truong Hiep",
    "website": "",
    "depends": ["om_service_master", "mail", "calendar", "portal"],
    "data": [
        "security/ir.model.access.csv",
        "security/appointment_security.xml",
        "data/sequence_data.xml",
        "data/email_templates.xml",
        "data/cron_jobs.xml",
        "views/service_appointment_views.xml",
        "views/dashboard_views.xml",
        "views/menu_views.xml",
    ],
    "images": [],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False,
}
