from django.shortcuts import render, HttpResponse, redirect
from .models import Breeder
from pedigree.models import Pedigree
from .forms import BreederForm
import csv

# @login_required(login_url="/members/login")
def breeder(request, breeder):
    breeder_details = Breeder.objects.get(prefix=breeder)
    pedigrees = Pedigree.objects.filter(breeder__prefix__exact=breeder)
    owned = Pedigree.objects.filter(current_owner__prefix__exact=breeder)
    return render(request, 'breeder.html', {'breeder_details': breeder_details,
                                            'pedigrees': pedigrees,
                                            'owned': owned})


# @login_required(login_url="/members/login")
def breeders(request):
    breeders = Breeder.objects
    return render(request, 'breeders.html', {'breeders': breeders})

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

def new_breeder_form(request):
    breeder_form = BreederForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if breeder_form.is_valid():
            new_breeder = Breeder()
            new_breeder.prefix = breeder_form['prefix'].value()
            new_breeder.contact_name = breeder_form['contact_name'].value()
            new_breeder.address = breeder_form['address'].value()
            new_breeder.phone_number1 = breeder_form['phone_number1'].value()
            new_breeder.phone_number2 = breeder_form['phone_number2'].value()
            new_breeder.email = breeder_form['email'].value()
            new_breeder.active = breeder_form['active'].value()
            new_breeder.save()

            return redirect('breeder', new_breeder.prefix)


    else:
        breeder_form = BreederForm()

    return render(request, 'new_breeder_form.html', {'breeder_form': breeder_form})