from django.db import models

# Create your models here.
class AdminAddFlight(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    duration = models.IntegerField()
    date = models.DateField(null=True)

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField  (max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"  # allows 