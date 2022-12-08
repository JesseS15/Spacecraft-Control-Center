from django.contrib import admin
from .models import Class, TestConductor, Sim, Subsystem

admin.site.register(Class)
admin.site.register(Subsystem)
admin.site.register(Sim)
admin.site.register(TestConductor)

