from django.conf import settings
from django.db import models 
from django.contrib.auth.models import Group

Group.add_to_class('sim_list', models.ManyToManyField("tc.Sim",verbose_name="Sim"))

###############################################################################
class TestConductor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    ##sim_list = models.ManyToManyField("tc.Sim", verbose_name=("Sim"), blank =True)
    def __str__(self):
        return self.user.username

###############################################################################
class Subsystem(models.Model):
    sys_name = models.CharField(default='', max_length=15)

    button_value = models.BooleanField(default=True)
    def __str__(self):
        return self.sys_name

###############################################################################
class Sim(models.Model):
    sim_name = models.CharField(default='', max_length=15)
    flight_operators = models.ManyToManyField("fo.FlightOperator", verbose_name=("Flight Operators"))
    sys_list = models.ManyToManyField(Subsystem)
    
    def __str__(self):
        return self.sim_name

###############################################################################
class Class(models.Model):
    class_name = models.CharField(default='', max_length=15)
    status = models.CharField(default='',max_length=15)
    flight_operators = models.ManyToManyField("fo.FlightOperator", verbose_name=("Flight Operator"))
    sims = models.ManyToManyField("Sim", verbose_name=("Sim"))

    def __str__(self):
        return self.class_name

    class Meta:
       verbose_name_plural = "Classes"