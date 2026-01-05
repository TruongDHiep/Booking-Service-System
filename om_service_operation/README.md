# Service Operations Module

## Overview

The **Service Operations** module (`om_service_operation`) is the business logic layer of the Service Booking Management System for Odoo 18.0.

This module handles all booking operations including appointment scheduling, workflow management, overlap checking, and customer communications through the integrated chatter system.

## Features

- ✅ **Appointment Management**: Complete booking lifecycle management
- ✅ **State Workflow**: Draft → Confirmed → Done with Cancel option
- ✅ **Overlap Detection**: Automatic time conflict checking
- ✅ **Calendar Views**: Visual scheduling and time management
- ✅ **Kanban Board**: Drag-and-drop workflow management
- ✅ **Chatter Integration**: Customer communication tracking
- ✅ **Activity Management**: Follow-up tasks and reminders
- ✅ **Automatic Numbering**: Sequential appointment references (BOOK/YYYY/NNNN)

## Module Information

- **Technical Name**: `om_service_operation`
- **Version**: 18.0.1.0.0
- **Author**: Truong Hiep
- **License**: LGPL-3
- **Category**: Services
- **Dependencies**: `om_service_master`, `mail`, `calendar`

## Models

### service.appointment

Main model for booking appointments with complete workflow support.

**Inheritance:**

- `mail.thread`: Chatter and message tracking
- `mail.activity.mixin`: Activity management

**Key Fields:**

- `reference` (Char): Auto-generated appointment reference
- `customer_id` (Many2one res.partner): Customer information
- `service_id` (Many2one booking.service): Selected service
- `booking_date` (Datetime): Start date and time
- `duration` (Float): Related from service
- `end_date` (Datetime): Computed end time
- `state` (Selection): Workflow status
- `price` (Monetary): Related from service
- `notes` (Text): Additional information

**Business Logic:**

1. **Overlap Checking**:

   - Validates appointments don't conflict in time
   - Checks same service resource availability
   - Excludes cancelled appointments from validation

2. **Past Date Prevention**:

   - Prevents booking appointments in the past
   - Validation on create and write

3. **Automatic Reference**:

   - Generated on creation using sequence
   - Format: BOOK/2025/0001

4. **Workflow Methods**:
   - `action_confirm()`: Confirm draft appointment
   - `action_done()`: Mark as completed
   - `action_cancel()`: Cancel appointment
   - `action_set_to_draft()`: Reset to draft

## Views

### List View

- Decorated rows based on state (green=done, blue=confirmed, muted=cancelled)
- All key information at a glance
- Sortable and filterable columns

### Form View

- **Header**: State buttons and statusbar
- **Sheet**: Customer info, service details, timing
- **Chatter**: Full communication history
- **Ribbons**: Visual indicators for cancelled/completed

### Calendar View

- Month/week/day views
- Color-coded by service
- Drag-and-drop scheduling
- Quick appointment details on click

### Kanban View

- Grouped by state (default)
- Card-based interface
- Essential information per card
- Quick status overview

### Search View

- Filters: Draft, Confirmed, Done, Cancelled
- Date filters: Today, This Week, Upcoming
- Group by: Customer, Service, Status, Date
- Smart search across reference and customer name

## Security

Full CRUD access granted to `base.group_user` (Internal Users).

## Installation

**Prerequisites:**

- `om_service_master` module must be installed first

**Steps:**

1. Copy the module to your Odoo addons directory
2. Restart Odoo server
3. Update Apps List
4. Search for "Service Operations"
5. Click Install

## Usage

### Creating an Appointment

1. Navigate to **Service Booking → Operations → Appointments**
2. Click **Create**
3. Select customer and service
4. Choose booking date and time
5. Add any special notes
6. Click **Save**
7. Click **Confirm** to confirm the appointment

### Managing Workflows

- **Draft**: Initial state, can be edited freely
- **Confirmed**: Customer confirmed, locked for editing
- **Done**: Service completed
- **Cancelled**: Appointment cancelled

### Calendar Management

- Access via **Service Booking → Operations → Calendar View**
- Drag appointments to reschedule
- Color coding helps identify services quickly
- Month/week/day views available

## Related Modules

- **om_service_master**: Master data (required)
- **om_website_booking**: Website frontend (PHASE 3)

## Development Notes

- Uses Odoo 18.0 `<list>` view type (not `<tree>`)
- Follows PEP8 coding standards
- Comprehensive docstrings and comments
- All constraint messages are user-friendly

## Support

For issues or questions, contact the module author.
