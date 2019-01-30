from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, render_to_response
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from .models import Pedigree, Breed, PedigreeAttributes
from breeder.models import Breeder
from .forms import PedigreeForm, AttributeForm, ImagesForm
from django.db.models import Q
import csv
from jinja2 import Environment, FileSystemLoader
from django.core.files.storage import FileSystemStorage

def home(request):
    total_pedigrees = Pedigree.objects.all().count()
    total_breeders = Breeder.objects.all().count()
    top_pedigrees = Pedigree.objects.all().order_by('-date_added')[:5]

    top_breeders = Breeder.objects.all()

    # breeders_totals = {}
    # for breeder in top_breeders:
    #     breeders_totals[breeder]['pedigree_count'] = Pedigree.objects.filter(breeder__prefix__exact=breeder).count()
    #     breeders_totals[breeder]['owned_count'] = Pedigree.objects.filter(current_owner__prefix__exact=breeder).count()

    return render(request, 'dashboard.html', {'total_pedigrees': total_pedigrees,
                                              'total_breeders': total_breeders,
                                              'top_pedigrees': top_pedigrees,
                                              'top_breeders': top_breeders,})

# @login_required(login_url="/members/login")
def search(request):
    return render(request, 'search.html')


class PedigreeBase(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['lvl1'] = Pedigree.objects.get(id=self.kwargs['pedigree_id'])

        # get any children
        context['children'] = Pedigree.objects.filter(Q(parent_father=context['lvl1']) | Q(parent_mother=context['lvl1']))

        try:
            context['lvl2_1'] = Pedigree.objects.get(reg_no=context['lvl1'].parent_mother)
        except:
            context['lvl2_1'] = ''

        try:
            context['lvl2_2'] = Pedigree.objects.get(reg_no=context['lvl1'].parent_father)
        except:
            context['lvl2_2'] = ''

        # lvl 3
        # 1
        try:
            context['lvl3_1'] = Pedigree.objects.get(name=context['lvl2_1'].parent_mother)
        except:
            context['lvl3_1'] = ''

        # 2
        try:
            context['lvl3_2'] = Pedigree.objects.get(name=context['lvl2_1'].parent_father)
        except:
            context['lvl3_2'] = ''

        # 3
        try:
            context['lvl3_3'] = Pedigree.objects.get(name=context['lvl2_2'].parent_mother)
        except:
            context['lvl3_3'] = ''

        # 4
        try:
            context['lvl3_4'] = Pedigree.objects.get(name=context['lvl2_2'].parent_father)
        except:
            context['lvl3_4'] = ''

        return context


# @method_decorator(login_required, name='dispatch')
class ShowPedigree(PedigreeBase):
    template_name = 'pedigree.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def search_results(request):
    if request.POST:
        search_string = request.POST['search']

        # lvl 1
        try:
            results = Pedigree.objects.filter(Q(reg_no__icontains=search_string.upper()) | Q(name__icontains=search_string))
        except ObjectDoesNotExist:
            breeders = Breeder.objects
            error = "No pedigrees found using: "
            return render(request, 'search.html', {'breeders': breeders,
                                                    'error': error,
                                                    'search_string': search_string})


        if len(results) > 1:
            return render(request, 'multiple_results.html', {'search_string': search_string,
                                                        'results': results})
        else:
            try:
                lvl1 = Pedigree.objects.get(Q(reg_no__icontains=search_string.upper()) | Q(name__icontains=search_string))
            except ObjectDoesNotExist:
                breeders = Breeder.objects
                error = "No pedigrees found using: "
                return render(request, 'search.html', {'breeders': breeders,
                                                       'error': error,
                                                       'search_string': search_string})

        return redirect('pedigree', pedigree_id=lvl1.id)

def new_pedigree_form(request):
    pedigree_objs = Pedigree.objects.all()
    breeder_objs = Breeder.objects.all()
    breed_objs = Breed.objects.all()

    pedigree_form = PedigreeForm(request.POST or None, request.FILES or None)
    attributes_form = AttributeForm(request.POST or None, request.FILES or None)
    image_form = ImagesForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        # check whether it's valid:
        if pedigree_form.is_valid() and attributes_form.is_valid() and image_form.is_valid():
            new_pedigree = Pedigree()
            try:
                new_pedigree.breeder = Breeder.objects.get(prefix=pedigree_form['breeder'].value())
            except ObjectDoesNotExist:
                pass
            try:
                new_pedigree.current_owner = Breeder.objects.get(prefix=pedigree_form['current_owner'].value())
            except ObjectDoesNotExist:
                pass
            new_pedigree.reg_no = pedigree_form['reg_no'].value()
            new_pedigree.name = pedigree_form['name'].value()
            try:
                new_pedigree.date_of_registration = pedigree_form['date_of_registration'].value() or None
            except:
                pass
            try:
                new_pedigree.dob = pedigree_form['date_of_birth'].value() or None
            except:
                pass
            new_pedigree.sex = pedigree_form['sex'].value()
            try:
                new_pedigree.dod = pedigree_form['date_of_death'].value() or None
            except:
                pass
            try:
                new_pedigree.mother = Pedigree.objects.get(reg_no=pedigree_form['mother'].value())
            except ObjectDoesNotExist:
                pass
            try:
                new_pedigree.father = Pedigree.objects.get(reg_no=pedigree_form['father'].value())
            except ObjectDoesNotExist:
                pass
            new_pedigree.description = pedigree_form['description'].value()
            new_pedigree.note = pedigree_form['note'].value()
            new_pedigree.save()

            new_pedigree_attributes = PedigreeAttributes()
            new_pedigree_attributes.reg_no = Pedigree.objects.get(reg_no=new_pedigree.reg_no)
            try:
                new_pedigree_attributes.breed = Breed.objects.get(breed_name=attributes_form['breed'].value())
            except ObjectDoesNotExist:
                pass

            eggs = attributes_form['eggs_per_week'].value()
            new_pedigree_attributes.eggs_per_week = int(eggs)
            new_pedigree_attributes.save()

            files = request.FILES.getlist('upload_images')
            fs = FileSystemStorage()
            for file in files:
                filename = fs.save(file.name, file)
            # uploaded_file_url = fs.url(filename)
            new_pedigree.save()
            return redirect('pedigree', new_pedigree.id)
    else:
        pedigree_form = PedigreeForm()

    reg_numbers = []
    for pedigree in pedigree_objs:
        reg_numbers.append(str(pedigree.reg_no))

    breeders = []
    for breeder in breeder_objs:
        breeders.append(str(breeder.prefix))

    breeds = []
    for breed in breed_objs:
        breeds.append(str(breed.breed_name))


    env = Environment(loader=FileSystemLoader('pedigree_demo/static/assets/plugins/typeahead.js-master'))
    template = env.get_template('typeahead.init.j2')

    with open('pedigree_demo/static/assets/plugins/typeahead.js-master/typeahead.init.js', 'w') as fh:
        fh.write(template.render(
            reg_numbers=reg_numbers,
            breeders=breeders,
            breeds=breeds
        ))

    return render(request, 'new_pedigree_form.html', {'pedigree_form': pedigree_form,
                                                      'attributes_form': attributes_form,
                                                      'image_form': image_form})


# @login_required(login_url="/members/login")
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
