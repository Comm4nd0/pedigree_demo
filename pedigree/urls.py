from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='pedigree_search'),
    path('<int:pedigree_id>', views.ShowPedigree.as_view(), name='pedigree'),
    path('results/', views.search_results, name='results'),
    # path('preview/<str:search_string>/', views.view_from_admin, name='preview'),
    path('breeder/<str:breeder>/', views.breeder, name='breeder'),
    path('breeders/', views.breeders, name='breeders'),
    path('pedigree_csv/', views.goat_csv, ),
    path('breeder_csv/', views.breeder_csv, )
]
