# -*- coding: utf-8 -*-
"""
Availability API Controller

JSON API endpoints for checking time slot availability.
Separated from main controller for better organization.
"""

from odoo import http
from odoo.http import request
from datetime import datetime, timedelta
import pytz


class AvailabilityAPI(http.Controller):
    """
    API Controller for Availability Checking.
    
    Provides JSON endpoints for frontend AJAX calls.
    """
    
    @http.route('/booking/check_availability', type='json', auth='public', methods=['POST'])
    def check_availability(self, service_id, date, **kwargs):
        """
        Check time slot availability for a specific service and date.
        
        Args:
            service_id: ID of the service
            date: Date string in YYYY-MM-DD format
            
        Returns:
            JSON with available time slots and their status
        """
        try:
            # Get user's timezone (default to UTC+7 for Vietnam)
            user_tz = request.env.user.tz or 'Asia/Ho_Chi_Minh'
            timezone = pytz.timezone(user_tz)
            
            # Parse the date in user's timezone
            selected_date = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Get service
            service = request.env['booking.service'].sudo().browse(int(service_id))
            if not service.exists():
                return {'error': 'Service not found'}
            
            # Define time slots (8 AM to 5 PM, hourly)
            business_hours = list(range(8, 17))  # 8:00 to 16:00 (last slot at 4 PM)
            
            slots = []
            Appointment = request.env['service.appointment'].sudo()
            
            # Get current time in user's timezone
            now_utc = datetime.now(pytz.UTC)
            now_local = now_utc.astimezone(timezone)
            
            for hour in business_hours:
                # Create datetime in user's LOCAL timezone
                slot_datetime_naive = datetime.combine(selected_date, datetime.min.time())
                slot_datetime_naive = slot_datetime_naive.replace(hour=hour, minute=0, second=0)
                
                # Localize to user's timezone
                slot_datetime_local = timezone.localize(slot_datetime_naive)
                
                # Convert to UTC for Odoo (Odoo stores in UTC)
                slot_datetime_utc = slot_datetime_local.astimezone(pytz.UTC)
                
                # Remove timezone info for Odoo (naive datetime)
                slot_datetime = slot_datetime_utc.replace(tzinfo=None)
                
                # Calculate end time
                end_datetime = slot_datetime + timedelta(hours=service.duration)
                
                # Check if slot is in the past (compare in local timezone)
                is_past = slot_datetime_local < now_local
                
                # Check availability
                has_overlap, _, error_msg = Appointment.check_overlap(
                    booking_date=slot_datetime,
                    end_date=end_datetime,
                    service_id=service.id
                )
                
                # Count current bookings for this slot
                current_bookings = Appointment.search_count([
                    ('service_id', '=', service.id),
                    ('state', 'not in', ['cancel']),
                    '|',
                    '&',
                    ('booking_date', '<', end_datetime),
                    ('end_date', '>', slot_datetime),
                    '&',
                    ('booking_date', '=', slot_datetime),
                    ('end_date', '=', end_datetime),
                ])
                
                # Return LOCAL time for display (frontend will show this)
                slot_info = {
                    'time': slot_datetime_local.strftime('%H:%M'),
                    'display': slot_datetime_local.strftime('%I:%M %p'),  # 08:00 AM
                    'datetime': slot_datetime_local.strftime('%Y-%m-%dT%H:%M'),  # Local time for frontend
                    'available': not has_overlap and not is_past,
                    'is_past': is_past,
                    'is_full': has_overlap,
                    'current_bookings': current_bookings,
                    'max_capacity': service.max_concurrent_bookings,
                }
                
                slots.append(slot_info)
            
            return {
                'slots': slots,
                'service_name': service.name,
                'duration': service.duration,
                'timezone': user_tz,
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
