from django.db import models
import static.testModule
from django.contrib.auth.models import User

class simulation():
    testArgument = "red"
    sim = static.testModule.testClass(testArgument)

class TestConductor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(blank=True)

    def __str__(self):
        return self.user.username
