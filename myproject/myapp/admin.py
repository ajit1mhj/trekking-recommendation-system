from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Booking

# UserProfile Admin Configuration
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'location')  # Display these fields in the list view
    search_fields = ('user__username', 'full_name', 'location')  # Enable search by username, full name, and location
    list_filter = ('location',)  # Filter users by location
    readonly_fields = ('user',)  # Make the 'user' field readonly

# Register the UserProfile model
admin.site.register(UserProfile, UserProfileAdmin)

# Booking Admin Configuration
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'trek_name', 'start_date', 'end_date', 'booking_date')  # Display these fields in the list view
    search_fields = ('user__username', 'trek_name')  # Search by user and trek name
    list_filter = ('start_date', 'end_date', 'booking_date')  # Enable filtering by dates

# Register the Booking model
admin.site.register(Booking, BookingAdmin)
