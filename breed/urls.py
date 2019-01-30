from django.urls import path

from . import views

urlpatterns = [
    path('', views.breeds, name='breeds'),
    path('new_breed/', views.new_breed_form, name='new_breed_form'),
]
