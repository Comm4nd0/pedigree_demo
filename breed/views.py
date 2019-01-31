from django.shortcuts import render, redirect, get_object_or_404
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


def edit_breed_form(request, breed_id):
    breed = get_object_or_404(Breed, id=breed_id)
    breed_form = BreedForm(request.POST or None, request.FILES or None, instance=breed)

    if request.method == 'POST':
        if breed_form.is_valid():
            breed_form.save()

            return redirect('breeds')


    else:
        breed_form = BreedForm()

    return render(request, 'edit_breed_form.html', {'breed_form': breed_form,
                                                    'breed': breed})