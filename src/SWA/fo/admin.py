# STaTE
# File: fo/admin.py
# Purpose: This file defines which models from the fo Django app are visible on the admin page

from django.contrib import admin
from .models import FlightOperator

admin.site.register(FlightOperator)