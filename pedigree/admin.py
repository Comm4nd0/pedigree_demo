from django.contrib import admin
from .models import Pedigree, PedigreeImage, PedigreeAttributes, Breed
from django.urls import reverse


class PedigreeAttributesInline(admin.StackedInline):
    model = PedigreeAttributes

class PedigreeImagesInline(admin.TabularInline):
    model = PedigreeImage
    extra = 3


class PedigreeAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'name', 'breeder', 'notes')
    list_display_links = ('name', 'breeder', 'reg_no')
    list_filter = ('date_of_registration', 'breeder', 'current_owner', 'date_added')
    search_fields = ['name', 'reg_no']
    ordering = ['reg_no']
    empty_value_display = '-empty-'
    fields = (('breeder', 'current_owner'),
              ('reg_no', 'name'),
              ('description',),
              ('date_of_registration',),
              ('dob',),
              ('dod',),
              'sex',
              ('parent_father', 'parent_mother'),
              'notes',)
    save_on_top = True
    inlines = [ PedigreeAttributesInline, PedigreeImagesInline ]


admin.site.register(Pedigree, PedigreeAdmin)

admin.site.register(PedigreeImage)

admin.site.register(PedigreeAttributes)

admin.site.register(Breed)