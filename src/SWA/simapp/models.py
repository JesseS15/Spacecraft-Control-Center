from django.conf import settings
from django.db import models
from Simulation.SimObject import SimObject
from Simulation.MissionScript import MissionScript

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

    flight_operators = models.ManyToManyField("fo.FlightOperator", default='', verbose_name=("Flight Operators"), blank=True)

    sys_list = models.ManyToManyField(Subsystem, verbose_name=("Subsystem"), blank=True)
    
    display_buffer = models.ManyToManyField("DisplayBufferItem", verbose_name=("Display buffer"), blank = True)
    
    def __str__(self):
        self.sim_object = SimObject(self.sim_name)
        return self.sim_name
    
    
