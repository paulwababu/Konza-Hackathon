from django.db import models

# Create your models here.
class Stock(models.Model):
    model = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    pieces = models.IntegerField(default='0', blank=True, null=True)
    unitPrice = models.FloatField(default='0', blank=True, null=True)
    
    def __str__(self):
        return self.model + ' ' + str(self.category) + ' ' + str(self.pieces) + ' ' + str(self.unitPrice)