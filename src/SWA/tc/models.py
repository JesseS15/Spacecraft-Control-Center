from django.conf import settings
from django.db import models 
from django.contrib.auth.models import Group

from simapp.models import Sim

Group.add_to_class('sim_list', models.ManyToManyField("simapp.Sim",verbose_name="Sim"))

###############################################################################
class TestConductor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username

###############################################################################
class Class(models.Model):
    class_name = models.CharField(default='', max_length=15)
    code = models.CharField(default='', max_length=15)
    status = models.CharField(default='',max_length=15)
    flight_operators = models.ManyToManyField("fo.FlightOperator", verbose_name=("Flight Operator"))
    sims = models.ManyToManyField("simapp.Sim", verbose_name=("Sim"))

    def __str__(self):
        return self.class_name

    class Meta:
       verbose_name_plural = "Classes"