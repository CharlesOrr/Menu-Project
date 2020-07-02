from django.urls import path

from . import views

app_name = 'menus'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/', views.RetrieveView.as_view(), name='retrieve'),
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', views.UpdateView.as_view(), name='update'),
]