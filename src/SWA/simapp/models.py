from django.conf import settings
from django.db import models

import random
from django.core.validators import MinValueValidator, MaxValueValidator
#settings.configure()

#class emptyfd(models.Model):
    #flight_director = models.ManyToManyField("fo.FlightOperator", related_name="flight_director",default='', verbose_name=("Flight Director"), blank=True)

###############################################################################
class CommandBufferItem(models.Model):
    buffer_item = models.CharField(default='', max_length=10)
    print(buffer_item)
    def __str__(self):
        return self.buffer_item

###############################################################################
class DisplayBufferItem(models.Model):
    buffer_item = models.CharField(default='', max_length=10)
    print(buffer_item)
    def __str__(self):
        return self.buffer_item
    
###############################################################################
class Subsystem(models.Model):
    sys_name = models.CharField(default='', max_length=15)
    button_value = models.BooleanField(default=True)
    command_buffer = models.ManyToManyField("CommandBufferItem", verbose_name=("command buffer"), blank = True)

    def __str__(self):
        return self.sys_name

###############################################################################
class Mission(models.Model):
    mission_name = models.CharField(default='', max_length=15)
    
    # Roll range: -180, 180
    # Pitch range: -90, 90
    # Yaw rangeL -180, 180
    final_roll = models.IntegerField(default=random.randint(-180,180), validators=[MinValueValidator(-180),MaxValueValidator(180)], blank=True)
    final_pitch = models.IntegerField(default=random.randint(-90,90), validators=[MinValueValidator(-90),MaxValueValidator(90)], blank=True)
    final_yaw = models.IntegerField(default=random.randint(-180,180), validators=[MinValueValidator(-180),MaxValueValidator(180)], blank=True)

    # 0 is prime meridian
    start_longitude = models.IntegerField(default=random.randint(-180,180), validators=[MinValueValidator(-180),MaxValueValidator(180)], blank=True)
    final_longitude = models.IntegerField(default=random.randint(-180,180), validators=[MinValueValidator(-180),MaxValueValidator(180)], blank=True)
    
    def __str__(self):
        return self.mission_name

###############################################################################
class Sim(models.Model):

    sim_name = models.CharField(default='', max_length=15)
    mission_script = models.ForeignKey(Mission, null=True, on_delete=models.CASCADE)

    flight_director = models.ManyToManyField("fo.FlightOperator", related_name="flight_director",default='', verbose_name=("Flight Director"), blank=True)
    director_command_buffer = models.ManyToManyField("CommandBufferItem", related_name="director_command_buffer", verbose_name=("Flight Director Command Buffer"), blank = True)
    
    COMMS_fo = models.ManyToManyField("fo.FlightOperator", related_name="comms_fo",default='', verbose_name=("Comms Flight Operator"), blank=True)
    COMMS_command_buffer = models.ManyToManyField("CommandBufferItem", related_name="COMMS_command_buffer", verbose_name=("COMMS Command Buffer"), blank = True)
    
    ACS_fo = models.ManyToManyField("fo.FlightOperator", related_name="acs_fo",default='', verbose_name=("ACS Flight Operator"), blank=True)
    ACS_command_buffer = models.ManyToManyField("CommandBufferItem", related_name="ACS_command_buffer", verbose_name=("ACS Command Buffer"), blank = True)
    
    EPS_fo = models.ManyToManyField("fo.FlightOperator", related_name="eps_fo",default='', verbose_name=("EPS Flight Operator"), blank=True)
    EPS_command_buffer = models.ManyToManyField("CommandBufferItem", related_name="EPS_command_buffer", verbose_name=("EPS Command Buffer"), blank = True)
    
    TCS_fo = models.ManyToManyField("fo.FlightOperator", related_name="tcs_fo",default='', verbose_name=("TCS Flight Operator"), blank=True)
    TCS_command_buffer = models.ManyToManyField("CommandBufferItem", related_name="TCS_command_buffer", verbose_name=("TCS Command Buffer"), blank = True)
    
    sys_list = models.ManyToManyField(Subsystem, verbose_name=("Subsystem"), blank=True)

    display_buffer = models.ManyToManyField("DisplayBufferItem", verbose_name=("Display Buffer"), blank = True)

    sim_identifier = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.sim_name