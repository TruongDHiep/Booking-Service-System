# Odoo 18 Service Booking System

A professional, modular booking management system for Odoo 18 with website integration.

##  Features

- **Multi-Module Architecture**: 4 specialized modules with clear separation of concerns
- **Website Integration**: Beautiful, responsive booking interface for customers
- **Advanced Security**: Role-based access control with portal integration
- **Email Automation**: Automated reminders and confirmation emails
- **Sales Integration**: Direct integration with Odoo Sales module
- **Real-time Availability**: Smart capacity management and overlap detection
- **Portal Access**: Customers can view and manage their bookings
- **Analytics Dashboard**: Pivot and graph views for booking insights

##  Modules

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

## 🚀 Installation

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

##  Security

### Access Groups

- **Appointment User**: Can create and manage own appointments
- **Appointment Manager**: Full access to all appointments
- **Portal**: Read-only access to own bookings

### Record Rules

- Users: See only their created appointments
- Managers: See all appointments
- Portal users: See only bookings linked to their partner

##  Configuration

### Email Templates

Customize email templates in: `om_service_operation/data/email_templates.xml`

### Cron Jobs

- **Reminder Emails**: Daily at 8 AM
- **Completion Emails**: Daily at 10 PM

Configure in: `om_service_operation/data/cron_jobs.xml`

##  Author

**Truong Hiep**

