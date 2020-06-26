from django.forms import ModelForm, Form, ModelChoiceField
from django.forms import formset_factory, modelformset_factory
from django.db import models
from .models import Menu, Item

class RestaurantForm(ModelForm):
    class Meta:
        model = Menu
        fields = ['restaurant_name']
    # restaurant_name = models.CharField(max_length=100)


class CreateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_text', 'meal_type', 'price']

CreateFormSet = modelformset_factory(Item, fields=('item_name', 'item_text', 'meal_type', 'price'),extra=5,)