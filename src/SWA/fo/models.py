from django.conf import settings
from django.db import models

class FlightOperator(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

        

    def __str__(self):
        return self.user.username
