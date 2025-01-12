from django import forms
from .models import Airport, Flight

class AdminAddFlightForm(forms.Form):
    origin = forms.ModelChoiceField(queryset=Airport.objects.all(), label="Origin Airport")
    destination = forms.ModelChoiceField(queryset=Airport.objects.all(), label="Destination Airport")
    duration = forms.IntegerField(label="Flight Duration (minutes)")
    date = forms.DateField(widget=forms.SelectDateWidget)
    price = forms.DecimalField(label="Price (USD)", max_digits=13, decimal_places=2)

class FlightFilterForm(forms.Form):
    airport = forms.ModelChoiceField(queryset=Airport.objects.all(), empty_label="Select an airport", widget=forms.Select(attrs={'class': 'form-select'}))
    filter_choice = forms.ChoiceField(choices=[
        ('departures', 'Departures'),
        ('arrivals', 'Arrivals')
    ],  widget=forms.Select(attrs={'class': 'form-select'})
    )

class BookForm(forms.Form):
    first = forms.CharField(max_length=64, label="First Name")
    last = forms.CharField(max_length=64, label="Last Name")

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=13, decimal_places=2, label="Deposit Amount")
