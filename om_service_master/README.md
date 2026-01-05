# Service Master Data Module

## Overview

The **Service Master Data** module (`om_service_master`) is the foundation layer of the Service Booking Management System for Odoo 18.0.

This module provides master data management capabilities for services without implementing booking business logic. It follows the separation of concerns principle as part of a multi-module architecture.

## Features

-  **Service Catalog Management**: Create and manage service offerings
-  **Pricing Configuration**: Set prices with multi-currency support
-  **Duration Settings**: Define service duration in hours
-  **Image Gallery**: Add representative images for each service
-  **Data Validation**: Built-in constraints for duration and pricing
-  **Archive Support**: Archive services without deletion

## Module Information

- **Technical Name**: `om_service_master`
- **Version**: 18.0.1.0.0
- **Author**: Truong Hiep
- **License**: LGPL-3
- **Category**: Services
- **Dependencies**: `base`

## Models

### booking.service

Main model for service master data:

**Fields:**

- `name` (Char, Required): Service name
- `image` (Image): Service representative image
- `duration` (Float, Required): Service duration in hours
- `price` (Monetary, Required): Service price
- `currency_id` (Many2one): Currency reference
- `active` (Boolean): Archive status
- `description` (Text): Detailed service description

**Constraints:**

- Duration must be greater than 0 hours
- Price cannot be negative

## Views

- **Tree View**: List of services with name, duration, and price
- **Form View**: Detailed service form with image and organized field groups
- **Search View**: Advanced search with filters for active/archived services and price sorting

## Security

Full CRUD access granted to `base.group_user` (Internal Users).

## Installation

1. Copy the module to your Odoo addons directory
2. Restart Odoo server
3. Update Apps List
4. Search for "Service Master Data"
5. Click Install

## Related Modules

- **om_service_operation**: Implements booking business logic (PHASE 2)
- **om_website_booking**: Provides website frontend for customer bookings (PHASE 3)

## Architecture

This module is part of a **Multi-Module Architecture**:

```
om_service_master (Foundation Layer)
    ↓
om_service_operation (Business Logic Layer)
    ↓
om_website_booking (Presentation Layer)
```

## Development Notes

- Follows **PEP8** coding standards
- Uses `snake_case` for variables and functions
- Uses `PascalCase` for class names
- XML IDs follow pattern: `module_name.model_name_view_type`

## Support

For issues or questions, contact the module author.
