from django.contrib import admin
from .models import Sim, DisplayBufferItem, CommandBufferItem

admin.site.register(Sim)
admin.site.register(DisplayBufferItem)
admin.site.register(CommandBufferItem)
