import logging

from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

logger = logging.getLogger(__name__)

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

    passenger_id = None
    if request.user.is_authenticated:
        try:
            passenger_id = request.user.passenger.id  # Retrieve the associated Passenger
        except Passenger.DoesNotExist:
            # Optional: Create a passenger profile automatically for new users
            passenger = Passenger.objects.create(
                user=request.user,
                first=request.user.first_name or request.user.username,
                last=request.user.last_name or "",
                balance=0.00
            )
            passenger_id = passenger.id

    if form.is_valid():
        airport = form.cleaned_data['airport']
        filter_choice = form.cleaned_data['filter_choice']
        
        if filter_choice == 'departures':
            flights = flights.filter(origin=airport)
        elif filter_choice == 'arrivals':
            flights = flights.filter(destination=airport)

    return render(request, 'airlineapp/index.html', {
        'form': form,
        'flights': flights,
        'passenger_id': passenger_id,  # Dynamic based on the logged-in user
    })

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist")
    return render(request, "airlineapp/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all()
    })

def book(request, flight_id):
    flight = Flight.objects.get(pk=flight_id)

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            # Get the logged-in user's details
            username = request.user.username

            # Check if passenger exists, if not create a new one
            passenger, created = Passenger.objects.get_or_create(
                user=request.user,
                defaults={'first': username, 'last': "", 'balance': 0.00}
            )

            # Check if passenger has sufficient funds
            if passenger.balance < flight.price:
                return render(request, "airlineapp/book.html", {
                    "form": form,
                    "flight": flight,
                    "error": "Insufficient funds to book this flight."
                })

            # Deduct flight price and book the flight
            passenger.balance -= flight.price
            passenger.save()
            flight.passengers.add(passenger)

            return HttpResponseRedirect(f"/{flight_id}/")
    else:
        form = BookForm()

    return render(request, "airlineapp/book.html", {
        "form": form,
        "flight": flight,
        "username": request.user.username  # Pass username to template
    })

def deposit(request, passenger_id):
    passenger = get_object_or_404(Passenger, pk=passenger_id)
    
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            passenger.balance += amount
            passenger.save()
            return HttpResponseRedirect(f"/")  # Redirect to passenger details
    else:
        form = DepositForm()

    return render(request, "airlineapp/deposit.html", {
        "form": form,
        "passenger": passenger
    })

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create a Passenger profile
            Passenger.objects.create(
                user=user,
                first=user.username,
                last="",
                balance=0.00
            )
            auth_login(request, user)
            return redirect('flight_filter')
    else:
        form = UserCreationForm()
    return render(request, 'airlineapp/signup.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('flight_filter')
    else:
        form = AuthenticationForm()
    return render(request, 'airlineapp/login.html', {'form': form})

def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('flight_filter')
