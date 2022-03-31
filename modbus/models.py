from django.db import models
from EasyModbusPy.easymodbus.modbusClient import *

# Create your models here.
class Digital (models.Model):
    coil_value =models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.coil_value)
    
class Analog (models.Model):
    register_value =models.IntegerField(default=0)

    def __str__(self):
        return str(self.register_value)
    