from django.contrib import admin
from .models import TestConductor
from .models import Sim

admin.site.register(Sim)
admin.site.register(TestConductor)
