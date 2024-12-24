from django import forms
from .models import Airport

class AdminAddFlightForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=Airport.objects.all(), label="Origin Airport")
    destination = forms.ModelChoiceField(queryset=Airport.objects.all(), label="Destination Airport")
    duration = forms.IntegerField(label="Flight Duration (minutes)")
    date = forms.DateField(widget=forms.SelectDateWidget)

class FlightFilterForm(forms.Form):
    airport = forms.ModelChoiceField(queryset=Airport.objects.all(), empty_label="Select an airport")
    filter_choice = forms.ChoiceField(choices=[
        ('departures', 'Departures'),
        ('arrivals', 'Arrivals')
    ])