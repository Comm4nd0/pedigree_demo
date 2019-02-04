from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from pedigree import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('pedigree/', include('pedigree.urls')),
    path('breeders/', include('breeder.urls')),
    path('breeds/', include('breed.urls')),
    path('account/', include('account.urls')),
    path('support/', include('support.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
