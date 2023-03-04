from django.contrib import admin

from .models import Subsystem, Sim, Mission

# Adds to the admin page:
admin.site.register(Subsystem)
admin.site.register(Sim)
admin.site.register(Mission)
