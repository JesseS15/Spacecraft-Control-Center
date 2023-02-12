from django.contrib import admin
from .models import FlightOperator, Post, Like

admin.site.register(FlightOperator)
admin.site.register(Post)
admin.site.register(Like)