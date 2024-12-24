from django.shortcuts import render
from .forms import AdminAddFlightForm, FlightFilterForm
from .models import Flight, Airport
from django.http import HttpResponseRedirect

# Create your views here.
def flight_filter(request):
    """
    Renders the flight filter form.
    """
    form = FlightFilterForm()
    return render(request, "airlineapp/flight_filter.html", {
        "form": form
    })

def admin(request):
    if request.method == "POST":
        form = AdminAddFlightForm(request.POST)
        if form.is_valid():
            # Process the form data
            origin = form.cleaned_data["origin"]
            destination = form.cleaned_data["destination"]
            duration = form.cleaned_data["duration"]
            date = form.cleaned_data["date"]

            # Save the new flight
            Flight.objects.create(
                origin=origin,
                destination=destination,
                duration=duration,
                date=date
            )
            return HttpResponseRedirect("/airlineapp/results/")  # Redirect after success
    else:
        form = AdminAddFlightForm()

    return render(request, "airlineapp/admin.html", {
        "form": form
    })

def index(request):
    """
    Displays the filtered flight results.
    """
    form = FlightFilterForm(request.GET or None)
    flights = Flight.objects.all()  # Default to showing all flights

    if form.is_valid():
        airport = form.cleaned_data['airport']
        filter_choice = form.cleaned_data['filter_choice']
        
        if filter_choice == 'departures':
            flights = flights.filter(origin=airport)
        elif filter_choice == 'arrivals':
            flights = flights.filter(destination=airport)

    return render(request, 'airlineapp/index.html', {
        'form': form,
        'flights': flights
    })