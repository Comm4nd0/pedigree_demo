from django.contrib import admin
from django.urls import path, include
from pedigree import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('pedigree/', include('pedigree.urls')),
    path('members/', include('members.urls')),
]
