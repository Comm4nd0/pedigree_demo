from django.shortcuts import render, HttpResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.auth.decorators import login_required
from .models import Pedigree, Breeder
from django.db.models import Q
import csv


def home(request):
    return render(request, 'dashboard.html')

@login_required(login_url="/members/login")
def search(request):
    breeders = Breeder.objects
    return render(request, 'search.html', {'breeders': breeders})


def search_res(request):
    return results(request, search_string=None)


def view_from_admin(request, search_string):
    return results(request, search_string)


@login_required(login_url="/members/login")
def results(request, search_string):
    if request.POST:
        search_string = request.POST['search']

    # lvl 1
    try:
        lvl1 = Pedigree.objects.filter(Q(reg_no__icontains=search_string.upper()) | Q(name__icontains=search_string))
    except ObjectDoesNotExist:
        breeders = Breeder.objects
        error = "No pedigrees found using: "
        return render(request, 'search.html', {'breeders': breeders,
                                               'error': error,
                                               'search_string': search_string})

    count = 0
    for res in lvl1.all():
        count += 1

    if count > 1:
        return render(request, 'multiple_results.html', {'results': lvl1,
                                                         'search_string': search_string})

    try:
        lvl1 = Pedigree.objects.get(Q(reg_no__icontains=search_string.upper()) | Q(name__icontains=search_string))
    except ObjectDoesNotExist:
        breeders = Breeder.objects
        error = "No pedigrees found using: "
        return render(request, 'search.html', {'breeders': breeders,
                                               'error': error,
                                               'search_string': search_string})

    data = {}

    data['lvl1'] = lvl1

    try:
        lvl2_1 = Pedigree.objects.get(reg_no=lvl1.parent_mother)
        data['lvl2_1'] = lvl2_1

    except:
        data['lvl2_1'] = ''

    try:
        lvl2_2 = Pedigree.objects.get(reg_no=lvl1.parent_father)
        data['lvl2_2'] = lvl2_2


    except:
        data['lvl2_2'] = ''

    # lvl 3
    # 1
    try:
        lvl3_1 = Pedigree.objects.get(name=lvl2_1.parent_mother)
        data['lvl3_1'] = lvl3_1

    except:
        data['lvl3_1'] = ''

    # 2
    try:
        lvl3_2 = Pedigree.objects.get(name=lvl2_1.parent_father)
        data['lvl3_2'] = lvl3_2

    except:
        data['lvl3_2'] = ''

    # 3
    try:
        lvl3_3 = Pedigree.objects.get(name=lvl2_2.parent_mother)
        data['lvl3_3'] = lvl3_3

    except:
        data['lvl3_3'] = ''

    # 4
    try:
        lvl3_4 = Pedigree.objects.get(name=lvl2_2.parent_father)
        data['lvl3_4'] = lvl3_4

    except:
        data['lvl3_4'] = ''

    return render(request, 'results.html', data)


@login_required(login_url="/members/login")
def breeder(request, breeder):
    breeder_details = Breeder.objects.get(prefix=breeder)
    pedigrees = Pedigree.objects.filter(breeder__prefix__exact=breeder)
    owned = Pedigree.objects.filter(current_owner__prefix__exact=breeder)
    return render(request, 'breeder.html', {'breeder_details': breeder_details,
                                            'pedigrees': pedigrees,
                                            'owned': owned})


@login_required(login_url="/members/login")
def breeders(request):
    breeders = Breeder.objects
    return render(request, 'breeders.html', {'breeders': breeders})


@login_required(login_url="/members/login")
def goat_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedigree_db.csv"'

    writer = csv.writer(response)
    writer.writerow(['breeder',
                     'current_owner',
                     'reg_no',
                     'name',
                     'date_of_registration'
                     'dob',
                     'dod',
                     'sex',
                     'parent_father',
                     'Parent_mother',
                     'notes',
                     'image',])
    goat = Pedigree.objects
    for row in goat.all():
        writer.writerow([row.breeder,
                         row.current_owner,
                         row.reg_no,
                         row.name,
                         row.date_of_registration,
                         row.dob,
                         row.dod,
                         row.sex,
                         row.parent_father,
                         row.parent_mother,
                         row.notes,
                         row.image,])

    return response


def breeder_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="breeder_db.csv"'

    writer = csv.writer(response)
    writer.writerow(['prefix',
                     'contact_name',
                     'address',
                     'phone_number1',
                     'phone_number2',
                     'email',
                     'active'])
    breeder = Breeder.objects
    for row in breeder.all():
        writer.writerow([row.prefix,
                         row.contact_name,
                         row.address,
                         row.phone_number1,
                         row.phone_number2,
                         row.email,
                         row.active
                         ])

    return response