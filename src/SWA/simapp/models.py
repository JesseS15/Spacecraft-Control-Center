from django.conf import settings
from django.db import models

###############################################################################
class Subsystem(models.Model):
    sys_name = models.CharField(default='', max_length=15)

    button_value = models.BooleanField(default=True)
    def __str__(self):
        return self.sys_name

###############################################################################

class TCS(models.Model):
    is_working = models.BooleanField(default=True)


###############################################################################
class Sim(models.Model):
    sim_name = models.CharField(default='', max_length=15)
    flight_operators = models.ManyToManyField("fo.FlightOperator", verbose_name=("Flight Operators"))
    sys_list = models.ManyToManyField(Subsystem)
    
    def __str__(self):
        return self.sim_name
####################################################################
class Mission(models.Model):
    mission_name = models.CharField(default='', max_length=15)
    test_conductor = models.ManyToManyField("tc.TestConductor")

    def __str__(self):
        return self.mission_name

