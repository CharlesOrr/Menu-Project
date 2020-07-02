import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Menu(models.Model):
	restaurant_name: models.CharField = models.CharField(max_length=100)
	pub_date: models.DateTimeField = models.DateTimeField('date published')

	def __str__(self):
		return self.restaurant_name + ' Menu'

	def published_within_one_week(self):
		current_date = timezone.now()
		return current_date>= self.pub_date >= timezone.now() - datetime.timedelta(days=7)

	def get_absolute_url(self):
		return reverse('menus:index')

class Item(models.Model):
	menu: models.ForeignKey = models.ForeignKey(Menu, on_delete=models.CASCADE)
	item_name: models.CharField = models.CharField(max_length=100)
	item_text: models.CharField = models.CharField(max_length=300)
	meal_type: models.CharField = models.CharField(max_length=50)
	price: models.FloatField = models.FloatField()

	def __str__(self):
		return self.item_name