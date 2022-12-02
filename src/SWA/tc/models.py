from django.conf import settings
from django.db import models

class TestConductor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username

class Sim(models.Model):
    sim_name = models.CharField(default='', max_length=15)

    button_value = models.BooleanField(default=True)

    def __str__(self):
        return self.sim_name


###class Classes(models.Model,):
    ##name = models.CharField(default='-', max_length=15)
    ##status = models.CharField(default='',max_length=15)
    ##class Meta:
       ## verbose_name_plural = "Classes"