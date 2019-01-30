from django.shortcuts import render, redirect
from .models import Breed
from .forms import BreedForm


# @login_required(login_url="/members/login")
def breeds(request):
    breeds = Breed.objects
    return render(request, 'breeds.html', {'breeds': breeds})


def new_breed_form(request):
    breed_form = BreedForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if breed_form.is_valid():
            new_breed = Breed()
            new_breed.breed_name = breed_form['breed_name'].value()
            new_breed.save()

            return redirect('breeds')


    else:
        breed_form = BreedForm()

    return render(request, 'new_breed_form.html', {'breed_form': breed_form})

