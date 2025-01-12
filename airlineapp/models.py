from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class AdminAddFlight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()
    date = models.DateField(null=True)

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()
    date = models.DateField()
    price = models.DecimalField(max_digits=13, decimal_places=2, default=10.00)
    passengers = models.ManyToManyField('Passenger', blank=True, related_name="flights")

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination} (${self.price})"

    def is_valid(self):
        if self.origin != self.destination or self.price > 0 or self.duration >= 0:
            return True
        elif self.origin == self.destination:
            error = "Origin and destination cannot be the same."
            return False
        elif self.price <= 0:
            error = "Price must be greater than 0."
            return False
        elif self.duration < 0:
            error = "Duration must be 0 or greater."
            return False

class Passenger(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="passenger",
        null=True,  # Temporarily allow null
        blank=True,  # Temporarily allow blank
    )
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return f"{self.first} {self.last} (Balance: ${self.balance})"

