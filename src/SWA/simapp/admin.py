# STaTE
# File: simapp/admin.py
# Purpose: This file defines which models from the simapp Django app are visible on the admin page

from django.contrib import admin
from .models import Sim, Mission

admin.site.register(Sim)
admin.site.register(Mission)
