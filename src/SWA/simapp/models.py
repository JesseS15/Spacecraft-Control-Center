from django.conf import settings
from django.db import models

#settings.configure()


###############################################################################
class Buffer_Item(models.Model):
    buffer_item = models.CharField(default='', max_length=1)
    print(buffer_item)
    def __str__(self):
        return self.buffer_item

###############################################################################
class Console_Buffer(models.Model):
    buffer_list = models.ManyToManyField("Buffer_Item", verbose_name=("Buffer list"))
    #print(buffer_list)
    def __str__(self):
        return self.buffer_list

###############################################################################
class Subsys_Menu(models.Model):
    main_menu = {}
    sub_menu_1 = {}
    sub_menu_2 = {}
    sub_menu_3 = {}
    def __str__(self):
        return self.main_menu
    
class ACS_Menu(models.Model):
    menu = Subsys_Menu()
    menu.main_menu = {
        '1': 'Adjust CMG angles',
        '2': 'Stabilize SimCraft',
        '3': 'Telementary transfer',
    }
    menu.sub_menu_1 = {
        '1': 'Roll',
        '2': 'Pitch',
        '3': 'Yaw',
    }
    menu.sub_menu_2 = {
        '1': 'X',
        '2': 'Y',
        '3': 'Z'
    }
    
###############################################################################
class Subsystem(models.Model):
    sys_name = models.CharField(default='', max_length=15)
    button_value = models.BooleanField(default=True)
    subsys_console_buffer = models.ManyToManyField("Console_Buffer", verbose_name=("Subsystem Console buffer"))

    #subsys_menu = models.ManyToManyField("ACS_Menu", verbose_name=("ACS Menu"))

    def __str__(self):
        return self.sys_name

###############################################################################
class Mission(models.Model):
    mission_name = models.CharField(default='', max_length=15)
    # Mission form needs to be created in tc forms
    
    def __str__(self):
        return self.mission_name

###############################################################################
class Sim(models.Model):
    sim_name = models.CharField(default='', max_length=15)
    # Verbose_name is the name it shows up on the admin page under Sim
    
    mission_script = models.ForeignKey(Mission, default=1, on_delete=models.CASCADE)

    flight_operators = models.ManyToManyField("fo.FlightOperator", verbose_name=("Flight Operators"), blank=True)

    #subsys_list = models.ManyToManyField(Subsystem)
    #acs_subsys = models.ManyToManyField("Subsystem", verbose_name=("ACS Subsystem"))

    #command_buffer = models.ManyToManyField("Console_Buffer", verbose_name=("console buffer"))
    
    def __str__(self):
        return self.sim_name