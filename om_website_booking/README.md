# Website Service Booking Module

## Overview

The **Website Service Booking** module (`om_website_booking`) is the presentation layer of the Service Booking Management System for Odoo 18.0.

This module provides a public-facing website interface where customers can browse services and book appointments online without needing to log in.

## Features

- ✅ **Public Service Catalog**: Grid-based service listing with images and pricing
- ✅ **Online Booking Form**: User-friendly appointment scheduling
- ✅ **Customer Management**: Automatic customer creation/update
- ✅ **Real-time Validation**: Overlap checking and date validation
- ✅ **Confirmation Page**: Appointment details and reference number
- ✅ **Error Handling**: User-friendly error messages
- ✅ **Responsive Design**: Mobile-first, works on all devices
- ✅ **Modern UI/UX**: Gradient backgrounds, animations, smooth transitions
- ✅ **Form Validation**: Client-side and server-side validation

## Module Information

- **Technical Name**: `om_website_booking`
- **Version**: 18.0.1.0.0
- **Author**: Truong Hiep
- **License**: LGPL-3
- **Category**: Website/Website
- **Dependencies**: `om_service_operation`, `website`

## Controllers

### WebsiteBookingController

**File**: [main.py](file:///c:/Users/truon/Downloads/odoo-space/odoo/addons/om_website_booking/controllers/main.py)

#### Routes:

1. **`/booking`** (GET, Public)

   - Displays service catalog
   - Shows all active services
   - Template: `service_catalog`

2. **`/booking/service/<int:service_id>`** (GET, Public)

   - Shows booking form for specific service
   - Template: `booking_form`

3. **`/booking/create`** (POST, Public, CSRF Protected)

   - Processes booking submission
   - Creates/updates customer record
   - Creates appointment with validation
   - Redirects to success or error page

4. **`/booking/success/<int:appointment_id>`** (GET, Public)
   - Displays confirmation details
   - Template: `booking_success`

## Templates

### 1. Service Catalog (`service_catalog`)

**Features**:

- Modern grid layout (3 columns on desktop, 1 on mobile)
- Service cards with images
- Hover animations
- Price and duration display
- "Book Now" buttons

**Design Elements**:

- Gradient header banner
- Shadow effects on cards
- Responsive grid system
- Empty state handling

### 2. Booking Form (`booking_form`)

**Features**:

- Service information card
- Customer details section (name, email, phone)
- Date/time picker with minimum date constraint
- Optional notes field
- CSRF protection
- Loading state on submission

**Validation**:

- Required field validation
- Email format validation
- Future date validation
- Phone number formatting

### 3. Success Page (`booking_success`)

**Features**:

- Animated success icon
- Appointment reference number
- Complete booking details
- Confirmation message
- Action buttons (Book Another / Home)

### 4. Error Page (`booking_error`)

**Features**:

- Animated error icon
- Error message list
- Retry and navigation options
- User-friendly error descriptions

## Static Assets

### CSS (`booking.css`)

**Styling Highlights**:

- Custom gradient backgrounds
- Smooth hover transitions
- Card shadow effects
- Responsive breakpoints
- Animation keyframes
- Loading spinner
- Form styling

**Color Scheme**:

- Primary gradient: `#667eea` to `#764ba2`
- Success: `#28a745`
- Danger: `#dc3545`
- Neutral grays for text

### JavaScript (`booking.js`)

**Functionality**:

- Set minimum date to current datetime
- Future date validation
- Phone number formatting
- Form submission loading state
- Smooth scroll navigation
- Service card scroll animations

## User Flow

```
1. Customer visits /booking
   ↓
2. Browse service catalog
   ↓
3. Click "Book Now" on desired service
   ↓
4. Fill booking form (customer info + date/time)
   ↓
5. Submit form (POST /booking/create)
   ↓
6a. Success → /booking/success/{id}
   OR
6b. Error → Error page with details
```

## Security & Access

- **Public Access**: All routes are accessible without authentication
- **CSRF Protection**: Form submissions are CSRF-protected
- **Sudo Mode**: Backend operations use `sudo()` for public user
- **Validation**: Server-side validation prevents invalid bookings

## Business Logic

### Customer Handling

- Search for existing customer by email
- Create new customer if not found
- Update phone number if changed
- Set `customer_rank = 1` for new customers

### Appointment Creation

- Uses `service.appointment` model from `om_service_operation`
- Applies overlap validation automatically
- Sets initial state to `draft`
- Generates reference number via sequence

## Installation

**Prerequisites:**

- `om_service_master` module installed
- `om_service_operation` module installed
- Odoo Website module enabled

**Steps:**

1. Copy module to addons directory
2. Restart Odoo server
3. Update Apps List
4. Install "Website Service Booking"
5. Access `/booking` on your website

## Configuration

### Website Menu

A "Book a Service" menu item is automatically added to the main website navigation.

**To customize:**

1. Go to Website → Configuration → Menus
2. Edit "Book a Service" menu
3. Change sequence, parent, or URL as needed

## Testing

### Manual Testing Checklist:

1. **Service Catalog**:

   - Access `/booking` as public user
   - Verify all active services display
   - Check images, prices, durations
   - Test responsive layout

2. **Booking Form**:

   - Click "Book Now" on a service
   - Verify form loads correctly
   - Test all required field validation
   - Check date picker minimum date

3. **Create Appointment**:

   - Submit valid booking
   - Verify redirect to success page
   - Check appointment created in backend
   - Verify customer created/updated

4. **Overlap Validation**:

   - Create appointment for Service A at 10:00
   - Try booking Service A at 10:30 (should fail)
   - Verify error message displays

5. **Mobile Responsiveness**:
   - Test on mobile device or emulator
   - Verify layout adapts correctly
   - Check all buttons are clickable

## Customization

### Styling

Modify `static/src/css/booking.css` to change:

- Color scheme
- Layout spacing
- Animation effects
- Typography

### Templates

Edit XML templates in `views/website_booking_templates.xml` to:

- Change page structure
- Add/remove fields
- Modify content

### Controllers

Update `controllers/main.py` to:

- Add custom validation
- Modify business logic
- Add email notifications
- Integrate payment

## Related Modules

- **om_service_master**: Service catalog (required)
- **om_service_operation**: Booking logic (required)

## Support

For issues or questions, contact the module author.
