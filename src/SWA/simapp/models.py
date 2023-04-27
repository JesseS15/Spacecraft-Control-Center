# STaTE
# File: simapp/models.py
# Purpose: This file defines database objects for the simapp Django app

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import random

###############################################################################
class Mission(models.Model):
    mission_name = models.CharField(default='', max_length=15)
    verbose_name = models.CharField(default='', max_length=20)
    # Roll range: -180, 180
    final_roll = models.IntegerField(default=random.randint(-180,180), validators=[MinValueValidator(-180),MaxValueValidator(180)], blank=True)
    # Pitch range: -90, 90
    final_pitch = models.IntegerField(default=random.randint(-90,90), validators=[MinValueValidator(-90),MaxValueValidator(90)], blank=True)
    # Yaw range -180, 180
    final_yaw = models.IntegerField(default=random.randint(-180,180), validators=[MinValueValidator(-180),MaxValueValidator(180)], blank=True)

    def __str__(self):
        return self.mission_name

###############################################################################
STATUS_CHOICES= (
    ('ACTIVE','ACTIVE'),
    ('COMPLETE','COMPLETE'),
    ('INACTIVE', 'INACTIVE'),
)
class Sim(models.Model):
    sim_name = models.CharField(default='', max_length=10)
    
    mission_script = models.ForeignKey(Mission, null=True, on_delete=models.CASCADE)
    
    # thread_id of associated SimObject thread
    sim_identifier = models.IntegerField(default=0, blank=True)
    fo_list = models.ManyToManyField("fo.FlightOperator")
    status = models.CharField(default='ACTIVE',max_length=15, blank = True, choices=STATUS_CHOICES)
    # Flight Operators and their assigned subsytems
    flight_director = models.ForeignKey("fo.FlightOperator", related_name="flight_director",default='', verbose_name=("Flight Director (Payload Flight Operator)"), blank=True, on_delete=models.CASCADE)
    COMMS_fo = models.ForeignKey("fo.FlightOperator", related_name="comms_fo",default='', verbose_name=("Comms Flight Operator"), blank=True, on_delete=models.CASCADE)
    ACS_fo = models.ForeignKey("fo.FlightOperator", related_name="acs_fo",default='', verbose_name=("ACS Flight Operator"), blank=True, on_delete=models.CASCADE)    
    EPS_fo = models.ForeignKey("fo.FlightOperator", related_name="eps_fo",default='', verbose_name=("EPS Flight Operator"), blank=True, on_delete=models.CASCADE)
    TCS_fo = models.ForeignKey("fo.FlightOperator", related_name="tcs_fo",default='', verbose_name=("TCS Flight Operator"), blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.sim_name