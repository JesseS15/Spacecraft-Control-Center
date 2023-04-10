from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import random

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
    #final_longitude = models.IntegerField(default=random.randint(-180,180), validators=[MinValueValidator(-180),MaxValueValidator(180)], blank=True)
    
    def __str__(self):
        return self.mission_name

###############################################################################
class Sim(models.Model):

    sim_name = models.CharField(default='', max_length=10)
    
    mission_script = models.ForeignKey(Mission, null=True, on_delete=models.CASCADE)
    
    # thread_id of associated SimObject thread
    sim_identifier = models.IntegerField(default=0, blank=True)

<<<<<<< Updated upstream
    flight_director = models.ManyToManyField("fo.FlightOperator", related_name="flight_director",default='', verbose_name=("Flight Director (Payload Flight Operator)"), blank=True)
    director_command_buffer = models.ManyToManyField("CommandBufferItem", related_name="director_command_buffer", verbose_name=("Flight Director Command Buffer"), blank = True)
    
=======
    # Flight Operator roles
    flight_director = models.ManyToManyField("fo.FlightOperator", related_name="flight_director",default='', verbose_name=("Flight Director"), blank=True)
>>>>>>> Stashed changes
    COMMS_fo = models.ManyToManyField("fo.FlightOperator", related_name="comms_fo",default='', verbose_name=("Comms Flight Operator"), blank=True)
    ACS_fo = models.ManyToManyField("fo.FlightOperator", related_name="acs_fo",default='', verbose_name=("ACS Flight Operator"), blank=True)    
    EPS_fo = models.ManyToManyField("fo.FlightOperator", related_name="eps_fo",default='', verbose_name=("EPS Flight Operator"), blank=True)
    TCS_fo = models.ManyToManyField("fo.FlightOperator", related_name="tcs_fo",default='', verbose_name=("TCS Flight Operator"), blank=True)

    def __str__(self):
        return self.sim_name