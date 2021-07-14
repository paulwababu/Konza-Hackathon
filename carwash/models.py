from django.db import models

# Create your models here.
class CarWash(models.Model):
    licensePlate = models.CharField(max_length=50, blank=True, null=True)
    vehicleType = models.CharField(max_length=50, blank=True, null=True)
    created_date = models.DateTimeField(auto_now=True)
    amountPaid = models.IntegerField(default='0', blank=True, null=True)
    
    def __str__(self):
        return self.licensePlate + ' ' + str(self.vehicleType) + ' ' + str(self.created_date) + ' ' + str(self.amountPaid)