# STaTE
# File: tc/admin.py
# Purpose: This file defines which models from the tc Django app are visible on the admin page

from django.contrib import admin
from .models import Class, TestConductor

admin.site.register(Class)
admin.site.register(TestConductor)

