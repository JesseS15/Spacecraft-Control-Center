# STaTE
# File: tc/models.py
# Purpose: This file defines database objects for the tc Django app

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models 

from simapp.models import Sim

import string
import random

Group.add_to_class('sim_list', models.ManyToManyField("simapp.Sim",verbose_name="Sim"))

###############################################################################
class TestConductor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    missions = models.ManyToManyField("simapp.Mission", verbose_name=("Mission"), blank=True)
    classes = models.ManyToManyField("tc.Class", blank= True)
    def __str__(self):
        return self.user.username

###############################################################################
STATUS_CHOICES= (
    ('ACTIVE','ACTIVE'),
    ('COMPLETE','COMPLETE')
)
class Class(models.Model):
    class_name = models.CharField(default='', max_length=15, null=False)
    test = models.BooleanField(default=True)
    code = models.CharField(max_length=8, blank=True)
    status = models.CharField(default='ACTIVE',max_length=15, blank = True, choices=STATUS_CHOICES)
    flight_operators = models.ManyToManyField("fo.FlightOperator", verbose_name=("Flight Operator"), blank= True)
    tc = models.ManyToManyField("tc.TestConductor")
    # Classses only want sims, which have a mission
    sims = models.ManyToManyField("simapp.Sim", verbose_name=("Sim"), blank=True)
    missions = models.ManyToManyField("simapp.Mission", verbose_name=("Mission"),blank=True)

    def __str__(self):
        return self.class_name
    
    class Meta:
       verbose_name_plural = "Classes"