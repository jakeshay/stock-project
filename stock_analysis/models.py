from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
	symbol = models.CharField(max_length=5)
	date_added = models.DateTimeField(auto_now=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

	def __str__(self):
		return self.symbol