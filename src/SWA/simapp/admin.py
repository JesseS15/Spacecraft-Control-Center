from django.contrib import admin

from .models import Subsystem, Sim, Mission

# Shows on admin page under SimApp
# We dont want TC to be able to add subsystems
#admin.site.register(Subsystem)
admin.site.register(Sim)
admin.site.register(Mission)
