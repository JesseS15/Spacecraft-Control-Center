from django.conf import settings
from django.db import models

###############################################################################
class FlightOperator(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    sim_list = models.ManyToManyField("tc.Sim", verbose_name=("Sim"))

    def __str__(self):
        return self.user.username

class Post(models.Model):
    post_heading = models.CharField(max_length=200)
    post_text = models.TextField()
    def __str__(self):
        return str(self.post_heading)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)