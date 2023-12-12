# models.py

from django.db import models
import uuid 
class Device(models.Model):
    uid = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    name = models.CharField(max_length=100,null=False)


    def __str__(self):
        return self.name

class TemperatureReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=7, decimal_places=3) 
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.temperature)

class HumidityReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    humidity = models.DecimalField(max_digits=7, decimal_places=3) 
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.humidity)