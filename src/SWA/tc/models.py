from django.conf import settings
from django.db import models

class TestConductor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    
    def __str__(self):
        return self.user.username

###class Classes(models.Model,):
    ##name = models.CharField(default='-', max_length=15)
    ##status = models.CharField(default='',max_length=15)
    ##class Meta:
       ## verbose_name_plural = "Classes"