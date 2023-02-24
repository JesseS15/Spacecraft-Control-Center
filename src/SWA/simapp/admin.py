from django.contrib import admin

from .models import Subsystem, Sim, Mission

admin.site.register(Subsystem)
admin.site.register(Sim)
admin.site.register(Mission)
