from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.views import generic
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.contrib import messages

import datetime

from .models import Menu, Item

from .forms import CreateForm, CreateFormSet, RestaurantForm

class IndexView(generic.ListView):
    template_name = 'menus/index.html'
    context_object_name = 'menu_list'

    def get_queryset(self):
        time = timezone.now()
        return Menu.objects.filter(pub_date__gte=time - datetime.timedelta(days=7), pub_date__lte=time).order_by('-pub_date')[:10]

class CreateView(generic.CreateView):
    model = Item
    success_url = '/'
    template_name = 'menus/create.html'
    form_class = CreateForm

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super(CreateView, self).get_context_data(**kwargs)
        context['formset'] = CreateFormSet(queryset=Item.objects.none())
        context['restaurant_form'] = RestaurantForm()
        return context

    def post(self, request, *args, **kwargs):
        formset = CreateFormSet(request.POST)
        restaurant_form = RestaurantForm(data=request.POST)
        if formset.is_valid() and restaurant_form.is_valid():
            return self.form_valid(formset,restaurant_form)
        else:
            messages.error(request, 'Missing required fields')
            return render(request, 'menus/create.html', {
                'formset': formset, 
                'restaurant_form': restaurant_form,
            })

    def form_valid(self, formset, restaurant_form):
        restaurant = restaurant_form.cleaned_data['restaurant_name']
        menu = Menu(restaurant_name=restaurant, pub_date=timezone.now())
        menu.save()

        instances = formset.save(commit=False)
        for instance in instances:
            instance.menu = menu
            instance.save()
        return HttpResponseRedirect('/menus')

class RetrieveView(generic.DetailView):
    model = Menu
    template_name = 'menus/retrieve.html'
    context_object_name = 'menu'

    def get_queryset(self):
        """
        excludes menus that are to old or to be published in the future
        """
        now = timezone.now()
        return Menu.objects.filter(pub_date__lte=now, pub_date__gte=now - datetime.timedelta(days=7))

class UpdateView(generic.UpdateView):
    model = Menu
    success_url = '/'
    template_name = 'menus/create.html'
    form_class = CreateForm 

    def get_context_data(self, **kwargs):
        menu_id = self.kwargs.get('pk')
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['formset'] = CreateFormSet(queryset=Item.objects.filter(menu=menu_id))
        context['restaurant_form'] = RestaurantForm(initial={'restaurant_name': Menu.objects.get(pk=menu_id)})
        return context

    def post(self, request, *args, **kwargs):
        formset = CreateFormSet(request.POST)
        restaurant_form = RestaurantForm(data=request.POST)
        if formset.is_valid() and restaurant_form.is_valid():
            return self.form_valid(formset,restaurant_form)
        else:
            return render(request, 'menus/create.html', {
                'formset': formset, 
                'restaurant_form': restaurant_form,
                'error_message': 'Invalid Input'})

    def form_valid(self, formset, restaurant_form):
        menu_id = self.kwargs.get('pk')
        restaurant = restaurant_form.cleaned_data['restaurant_name']

        # retrieve Menu with id=menu_id and edit its data
        menu = Menu.objects.get(pk=menu_id)
        menu.restaurant_name = restaurant
        menu.pub_date = timezone.now()
        menu.save()

        instances = formset.save(commit=False)
        for instance in instances:
            instance.menu = menu
            instance.save()
        return HttpResponseRedirect('/menus')


class DeleteView(generic.DeleteView):
    template_name = 'menus/delete.html'
    model = Menu
    success_url = '/menus'