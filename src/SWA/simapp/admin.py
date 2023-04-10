from django.contrib import admin

from .models import Sim, Mission

# Shows on admin page under SimApp
admin.site.register(Sim)
admin.site.register(Mission)
