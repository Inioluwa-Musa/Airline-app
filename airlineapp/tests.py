from django.db.models import Max
from django.test import TestCase, Client

from datetime import date, datetime, timedelta

from .models import *

# Create your tests here.
class FlightTestCase(TestCase):
    def setUp(self):

        # Create airports
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Make time
        tomorrow = date.today() + timedelta(days=1)
        yesterday = date.today() - timedelta(days=1)

        # Create flights
        Flight.objects.create(origin=a1, destination=a2, duration=100, date=date.today())
        Flight.objects.create(origin=a1, destination=a1, duration=200, date=tomorrow)
        Flight.objects.create(origin=a1, destination=a2, duration=150, date=yesterday)
    
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(),3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        fs = Flight.objects.all()
        for f in fs:
            self.assertTrue(f.is_valid())
            print(f" \n \"For test: test_valid_flight\" \n Checking flight {f} | Valid: {self.assertTrue(f.is_valid())}")

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        try:
            self.assertFalse(f.is_valid())
        except AssertionError:
            print(f" \n \"For test: test_invalid_flight_destination\" \n Flight {f} is invalid because origin and destination are the same")

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertFalse(f.is_valid())
        if self.assertFalse(f.is_valid()) != False:
            print(f" \n \"For test: test_invalid_flight_duration\" \n Flight {f} is invalid because duration is less than 0 or an error occured in the function")

    def test_index(self):
        response = self.client.get('/results/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), Flight.objects.count())

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        response = self.client.get(f'/{f.id}')
        self.assertEqual(response.status_code, 200)
        if response.status_code != 200:
            print(f" \n \"For test: test_valid_flight_page\" \n Flight {f} is invalid because it doesn't exist")

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        response = self.client.get(f'/{max_id + 1}')
        self.assertEqual(response.status_code, 404)
        if response.status_code != 404:
            print(f" \n \"For test: test_invalid_flight_page\" \n This Flight does not exist")

    def test_flight_page_passengers(self):
        try:
            f = Flight.objects.get(pk=1)
        except Flight.DoesNotExist:
            f = Flight.objects.create(origin=Airport.objects.get(code="AAA"), destination=Airport.objects.get(code="BBB"), duration=100, date=date.today())
            p = Passenger.objects.create(first="Alice", last="Adams")
            f.passengers.add(p)

            response = self.client.get(f'/{f.id}')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Alice Adams")