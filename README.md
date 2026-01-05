# Odoo 18 Service Booking System

## Features

- **Multi-Module Architecture**: 4 specialized modules with clear separation of concerns
- **Website Integration**: Beautiful, responsive booking interface for customers
- **Advanced Security**: Role-based access control with portal integration
- **Email Automation**: Automated reminders and confirmation emails
- **Sales Integration**: Direct integration with Odoo Sales module
- **Real-time Availability**: Smart capacity management and overlap detection
- **Portal Access**: Customers can view and manage their bookings
- **Analytics Dashboard**: Pivot and graph views for booking insights

## Screenshots

### User Interface
<img width="1920" height="2741" alt="ảnh" src="https://github.com/user-attachments/assets/84db5eb3-4bf7-4c07-af6e-2cb47a18a424" />
<img width="1920" height="2121" alt="ảnh" src="https://github.com/user-attachments/assets/c8d7bc86-cb88-4498-bb0c-d27deb308155" />
<img width="1920" height="3546" alt="ảnh" src="https://github.com/user-attachments/assets/c8509807-c6e5-4d2e-9f2a-d90f2e00280d" />
<img width="1920" height="2770" alt="ảnh" src="https://github.com/user-attachments/assets/77a16375-20d8-41f2-a6a9-8cf5901b8dc7" />
<img width="1920" height="1938" alt="ảnh" src="https://github.com/user-attachments/assets/f0d79c0a-f95a-41f8-b431-e9f491869c93" />

### User Portal 
<img width="1920" height="913" alt="ảnh" src="https://github.com/user-attachments/assets/8781659c-0db0-4c99-9729-17e06e861261" />
<img width="1920" height="913" alt="ảnh" src="https://github.com/user-attachments/assets/b17ff27e-734b-4017-9397-f93c5a84f4d5" />

### Admin Panel
<img width="1920" height="913" alt="ảnh" src="https://github.com/user-attachments/assets/6c5ee4b4-4027-457a-9d70-02a5a2525446" />
<img width="1920" height="913" alt="ảnh" src="https://github.com/user-attachments/assets/58ce4b62-5037-4d75-a303-e0758fc2fd06" />
<img width="1920" height="913" alt="ảnh" src="https://github.com/user-attachments/assets/8e809723-d320-4353-8077-8e10ca6023ef" />
<img width="1920" height="913" alt="ảnh" src="https://github.com/user-attachments/assets/773166c5-3a65-419d-81ba-1cc48d801736" />
<img width="1920" height="913" alt="ảnh" src="https://github.com/user-attachments/assets/f6fe2818-f74e-4c65-badf-24289d75b317" />
<img width="1920" height="913" alt="ảnh" src="https://github.com/user-attachments/assets/cc8f9324-41d5-433a-8767-1157fc4f8138" />

## Modules

### 1. `om_service_master` - Data Layer

Foundation module for service master data management.

**Features:**

- Service catalog with pricing
- SEO-friendly URL slugs
- Product integration for sales
- Capacity configuration

### 2. `om_service_operation` - Business Logic Layer

Core booking operations and workflow management.

**Features:**

- Complete booking workflow (Draft → Confirmed → Done/Cancel)
- Overlap detection with capacity management
- Email notifications (confirmation, reminders, completion)
- Cron jobs for automated tasks
- Activity management
- Advanced security groups and record rules

### 3. `om_service_sale` - Integration Layer

Bridge module connecting appointments with sales orders.

**Features:**

- Auto-generate quotations from confirmed appointments
- Smart buttons for easy navigation
- Duplicate prevention
- Automatic pricing sync

### 4. `om_website_booking` - Presentation Layer

Customer-facing website interface.

**Features:**

- Service catalog listing
- Detailed service pages
- Real-time booking form
- AJAX availability checking
- Confirmation page
- Responsive design

## Installation

### Prerequisites

- Odoo 18.0
- Python 3.10+
- PostgreSQL 12+

### Steps

1. Clone this repository into your Odoo addons directory:

```bash
cd /path/to/odoo/addons
git clone https://github.com/YOUR_USERNAME/booking_system.git
```

2. Restart Odoo server:

```bash
./odoo-bin -c odoo.conf --update=all
```

3. Install modules in order:
   - `om_service_master` (required first)
   - `om_service_operation`
   - `om_service_sale` 
   - `om_website_booking`

## Usage

### For Administrators

1. **Create Services**: Apps → Services → Service Master → Create
2. **Configure Pricing**: Set price and duration for each service
3. **Set Capacity**: Configure `max_concurrent_bookings` for capacity management
4. **Manage Bookings**: Apps → Services → Appointments

### For Customers

1. Visit: `https://yourdomain.com/booking`
2. Browse service catalog
3. Select service and time slot
4. Fill booking form
5. Access bookings via portal: `My Account → My Appointments`

##  Architecture

```
┌─────────────────────────────────────────┐
│     om_website_booking (Presentation)    │
│   - Controllers                          │
│   - Templates                            │
│   - Static Assets                        │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼────────┬──────────────┐
│  om_service_operation    │ om_service_  │
│  (Business Logic)        │ sale         │
│  - Workflow              │ (Integration)│
│  - Validation            │              │
│  - Email Service         │              │
└─────────────────┬────────┴──────────────┘
                  │
┌─────────────────▼───────────────────────┐
│     om_service_master (Data Layer)      │
│   - Service Model                       │
│   - Master Data                         │
└─────────────────────────────────────────┘
```

## Security

### Access Groups

- **Appointment User**: Can create and manage own appointments
- **Appointment Manager**: Full access to all appointments
- **Portal**: Read-only access to own bookings

### Record Rules

- Users: See only their created appointments
- Managers: See all appointments
- Portal users: See only bookings linked to their partner

## Configuration

### Email Templates

Customize email templates in: `om_service_operation/data/email_templates.xml`

### Cron Jobs

- **Reminder Emails**: Daily at 8 AM
- **Completion Emails**: Daily at 10 PM

Configure in: `om_service_operation/data/cron_jobs.xml`

## Author

**Truong Hiep**

