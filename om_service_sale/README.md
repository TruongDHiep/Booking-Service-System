# Service Sale Integration Module

## Overview

This module bridges the Service Booking system with Odoo Sales, enabling automatic quotation generation from confirmed appointments.

## Features

- **Generate Sale Orders**: Create quotations directly from confirmed appointments
- **Smart Button**: View linked sale orders with one click
- **Product Integration**: Automatically uses the product linked to the service
- **Duplicate Prevention**: Ensures only one quotation per appointment
- **State Validation**: Only confirmed appointments can generate quotations

## Installation

1. Ensure dependencies are installed:

   - `om_service_operation`
   - `sale_management`

2. Install the module:
   ```bash
   odoo-bin -d your_database -u om_service_sale
   ```

## Usage

### Creating a Quotation

1. Navigate to **Service Booking > Operations > Appointments**
2. Open a confirmed appointment
3. Click the **"Create Quotation"** button in the header
4. The system will:
   - Create a new Sale Order
   - Add a line with the service product
   - Link the SO to the appointment
   - Open the created quotation

### Viewing Linked Quotation

- Click the **"1 Quotation"** smart button at the top of the appointment form

## Business Rules

- **State Requirement**: Only `confirmed` appointments can generate quotations
- **Product Requirement**: The service must have a `Related Product` configured
- **One-to-One**: Each appointment can only generate one sale order
- **Pricing**: Sale order line uses the service's price (can be modified in SO)

## Technical Details

### Models

**service.appointment** (inherited)

- `sale_order_id`: Many2one link to generated sale order
- `sale_order_count`: Computed field for smart button

### Methods

- `action_create_sale_order()`: Generate SO with validation
- `action_view_sale_order()`: Open linked SO form

### Views

- Inherited form view with:
  - Smart button (icon: fa-usd)
  - Header button "Create Quotation"
  - Sale Order field in new group

## Error Handling

The module provides clear error messages for:

- Attempting to create SO from non-confirmed appointment
- Trying to create duplicate quotations
- Missing product configuration on service

## Future Enhancements

- Auto-confirm SO option
- Invoice generation trigger
- Payment status tracking
