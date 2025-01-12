from django.contrib import admin

from .models import *
# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin', 'destination', 'duration', 'date', 'price', )
    list_filter = ('origin', 'destination', 'date')
    search_fields = ('origin__city', 'destination__city', 'date')

class AirportAdmin(admin.ModelAdmin):
    list_display = ("id", "city", "code")

class PassengerAdmin(admin.ModelAdmin):
    """ filter_horizontal = ("flights", ) """
    list_display = ("id", "first", "last", "balance")

admin.site.register(Airport, AirportAdmin)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
