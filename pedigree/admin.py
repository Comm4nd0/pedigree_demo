from django.contrib import admin
from .models import Goat, Breeder
from django.urls import reverse


class GoatAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'name', 'breeder', 'notes')
    list_display_links = ('name', 'breeder', 'reg_no')
    list_filter = ('date_of_registration', 'breeder', 'current_owner')
    search_fields = ['name', 'reg_no']
    ordering = ['reg_no']
    empty_value_display = '-empty-'
    fields = (('breeder', 'current_owner'),
              ('reg_no', 'name'),
              ('date_of_registration', 'dob', 'dod'),
              'sex',
              ('sire', 'dam'),
              'notes',
              'image',
              ('min_milk_yield', 'max_milk_yield', 'avg_milk_yield'),
              ('first_prize', 'second_prize', 'third_prize'))
    save_on_top = True

    def view_on_site(self, Goat):
        url = reverse('preview', kwargs={'reg_no': Goat.reg_no})
        return 'http://35.178.2.225' + url


class BreederAdmin(admin.ModelAdmin):
    list_display = ('prefix', 'contact_name', 'address', 'phone_number1', 'phone_number2', 'email')
    list_display_links = ('prefix', 'contact_name', 'address', 'phone_number1', 'phone_number2', 'email')
    search_fields = ('prefix', 'contact_name', 'address', 'phone_number1', 'phone_number2', 'email')
    list_filter = ('active', 'prefix')
    ordering = ['prefix']
    empty_value_display = '-empty-'

    fieldsets = (
        ('Breeder details', {
            'fields': ('prefix', 'active')
        }),
        ('Contact options', {
            'fields': ('contact_name', 'address', 'phone_number1', 'phone_number2', 'email'),
        }),
    )
    save_on_top = True

    def view_on_site(self, Breeder):
        url = reverse('breeder', kwargs={'breeder': Breeder.prefix})
        return 'http://35.178.2.225' + url

admin.site.register(Goat, GoatAdmin)

admin.site.register(Breeder, BreederAdmin)