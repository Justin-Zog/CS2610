from django.db import models

class ConversionUnit(models.Model):
    unit = models.CharField(max_length=4)
    conversion_factor = models.FloatField()

    def __str__(self):
        return self.unit

 


