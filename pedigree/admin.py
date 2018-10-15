from django.contrib import admin
from .models import Pedigree, Breeder
from django.urls import reverse


class PedigreeAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'name', 'breeder', 'notes')
    list_display_links = ('name', 'breeder', 'reg_no')
    list_filter = ('date_of_registration', 'breeder', 'current_owner')
    search_fields = ['name', 'reg_no']
    ordering = ['reg_no']
    empty_value_display = '-empty-'
    fields = (('breeder', 'current_owner'),
              ('reg_no', 'name'),
              ('date_of_registration'),
              ('dob'),
              ('dod'),
              'sex',
              ('parent_father', 'parent_mother'),
              'notes',
              'image',)
    save_on_top = True

    # def view_on_site(self, Pedigree):
    #     url = reverse('preview', kwargs={'reg_no': Pedigree.reg_no})
    #     return 'http://localhost' + url


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

    # def view_on_site(self, Breeder):
    #     url = reverse('breeder', kwargs={'breeder': Breeder.prefix})
    #     return 'http://localhost' + url

admin.site.register(Pedigree, PedigreeAdmin)

admin.site.register(Breeder, BreederAdmin)