from django.conf import settings
from django.db import models
from simulation.SimObject import SimObject
from simulation.MissionScript import MissionScript

#settings.configure()


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
class Subsys_Menu(models.Model):
    main_menu = {}
    sub_menu_1 = {}
    sub_menu_2 = {}
    sub_menu_3 = {}
    def __str__(self):
        return self.main_menu
    
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
    # Mission form needs to be created in tc forms
    
    def __str__(self):
        self.mission_object = MissionScript(self.mission_name)
        return self.mission_name

###############################################################################
class Sim(models.Model):

    sim_name = models.CharField(default='', max_length=15)
    
    mission_script = models.ForeignKey(Mission, null=True, on_delete=models.CASCADE)
    
    flight_director = models.ManyToManyField("fo.FlightOperator", default='', verbose_name=("Flight Director"), blank=True)
    COMMS_fo = models.ManyToManyField("fo.FlightOperator", related_name="comms_fo",default='', verbose_name=("Comms Flight Operator"), blank=True)
    ACS_fo = models.ManyToManyField("fo.FlightOperator", related_name="acs_fo",default='', verbose_name=("ACS Flight Operator"), blank=True)
    EPS_fo = models.ManyToManyField("fo.FlightOperator", related_name="eps_fo",default='', verbose_name=("EPS Flight Operator"), blank=True)
    TCS_fo = models.ManyToManyField("fo.FlightOperator", related_name="tcs_fo",default='', verbose_name=("TCS Flight Operator"), blank=True)
    sys_list = models.ManyToManyField(Subsystem, verbose_name=("Subsystem"), blank=True)

    display_buffer = models.ManyToManyField("DisplayBufferItem", verbose_name=("Display buffer"), blank = True)


    def __str__(self):
        self.sim_object = SimObject(self.sim_name)
        return self.sim_name
#################################################

    
    
    
