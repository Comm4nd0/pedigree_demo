from django.contrib import admin
from .models import Pedigree, Breeder, PedigreeImage
from django.urls import reverse


class PedigreeImagesInline(admin.TabularInline):
    model = PedigreeImage
    extra = 3


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
              'notes',)
    save_on_top = True
    inlines = [ PedigreeImagesInline ]


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


admin.site.register(Pedigree, PedigreeAdmin)

admin.site.register(Breeder, BreederAdmin)

admin.site.register(PedigreeImage)