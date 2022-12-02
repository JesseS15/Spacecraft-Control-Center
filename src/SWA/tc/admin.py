from django.contrib import admin
from .models import TestConductor, Sim, Subsystem

admin.site.register(Subsystem)
admin.site.register(Sim)
admin.site.register(TestConductor)
