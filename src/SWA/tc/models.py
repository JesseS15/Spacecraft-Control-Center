from django.conf import settings
from django.db import models

class TestConductor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    sim_list = models.ManyToManyField("tc.Sim", verbose_name=("Sim"))
    def __str__(self):
        return self.user.username

class Subsystem(models.Model):
    sys_name = models.CharField(default='', max_length=15)

    button_value = models.BooleanField(default=True)
    def __str__(self):
        return self.sys_name

class Sim(models.Model):
    sim_name = models.CharField(default='', max_length=15)
    flight_operators = models.ManyToManyField("fo.FlightOperator", verbose_name=("Flight Operator"))
    sys_list = models.ManyToManyField(Subsystem)

    def __str__(self):
        return self.sim_name

###class Classes(models.Model,):
    ##name = models.CharField(default='-', max_length=15)
    ##status = models.CharField(default='',max_length=15)
    ##class Meta:
       ## verbose_name_plural = "Classes"