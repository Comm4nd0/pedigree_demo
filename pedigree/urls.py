from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='pedigree_search'),
    path('<int:pedigree_id>', views.ShowPedigree.as_view(), name='pedigree'),
    path('results/', views.search_results, name='results'),
    path('new_pedigree/', views.new_pedigree_form, name='new_pedigree_form'),
    path('<int:lvl1_id>/edit_pedigree/', views.edit_pedigree_form, name='edit_pedigree_form'),
    path('pedigree_csv/', views.goat_csv, ),
]
