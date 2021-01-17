from django.db import models
from django.contrib.auth.models import User

class PlaidKey(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # access_token = models.CharField(max_length=200)
    # item_id = models.CharField(max_length=200)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    access_token = models.CharField(max_length=200)
    item_id = models.CharField(max_length=200)

    def __str__(self):
        return "Access Token: "+self.access_token+" | Item ID: "+self.item_id
