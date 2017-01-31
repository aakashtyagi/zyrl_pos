from django.db import models
import datetime
# Create your models here.

class SquareCustomer(models.Model):
	name = models.CharField(max_length=100, default=None, blank=True)
	access_token = models.CharField(max_length=200,default=None, blank=True)
	location = models.CharField(max_length=100,default=None, blank=True)
	expiry_date = models.DateField(auto_now=False, auto_now_add=False,default=None,null=True)
