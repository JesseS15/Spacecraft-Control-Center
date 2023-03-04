from django.conf import settings
from django.db import models

###############################################################################
class FlightOperator(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    sim_list = models.ManyToManyField("simapp.Sim", verbose_name=("Sim"), blank=True)
    class_list = models.ManyToManyField("tc.Class", verbose_name = ("Class"), blank = True)
    def __str__(self):
        return self.user.username
    