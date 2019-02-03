from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from .models import Pedigree, PedigreeAttributes, PedigreeImage
from breed.models import Breed
from breeder.models import Breeder
from .forms import PedigreeForm, AttributeForm, ImagesForm
from django.db.models import Q
import csv
from jinja2 import Environment, FileSystemLoader
from django.core.files.storage import FileSystemStorage


def is_editor(user):
    return user.groups.filter(name='editor').exists() or user.is_superuser


@login_required(login_url="/account/login")
def home(request):
    editor = is_editor(request.user)
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
                                              'top_breeders': top_breeders,
                                              'editor': editor})


@login_required(login_url="/account/login")
def search(request):
    editor = is_editor(request.user)
    pedigrees = Pedigree.objects.all()
    return render(request, 'search.html', {'pedigrees': pedigrees,
                                           'editor': editor})



class PedigreeBase(LoginRequiredMixin, TemplateView):
    login_url = '/account/login'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['editor'] = is_editor(self.request.user)

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



class ShowPedigree(PedigreeBase):
    template_name = 'pedigree.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required(login_url="/account/login")
def search_results(request):
    if request.POST:
        editor = is_editor(request.user)
        search_string = request.POST['search']

        # lvl 1
        try:
            results = Pedigree.objects.filter(Q(reg_no__icontains=search_string.upper()) | Q(name__icontains=search_string))
        except ObjectDoesNotExist:
            breeders = Breeder.objects
            error = "No pedigrees found using: "
            return render(request, 'search.html', {'breeders': breeders,
                                                    'error': error,
                                                    'search_string': search_string,
                                                       'editor': editor})


        if len(results) > 1:
            return render(request, 'multiple_results.html', {'search_string': search_string,
                                                        'results': results,
                                                       'editor': editor})
        else:
            try:
                lvl1 = Pedigree.objects.get(Q(reg_no__icontains=search_string.upper()) | Q(name__icontains=search_string))
            except ObjectDoesNotExist:
                breeders = Breeder.objects
                error = "No pedigrees found using: "
                return render(request, 'search.html', {'breeders': breeders,
                                                       'error': error,
                                                       'search_string': search_string,
                                                       'editor': editor})

        return redirect('pedigree', pedigree_id=lvl1.id)


@login_required(login_url="/account/login")
@user_passes_test(is_editor)
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
                new_pedigree.parent_mother = Pedigree.objects.get(reg_no=pedigree_form['mother'].value())
            except ObjectDoesNotExist:
                pass
            try:
                new_pedigree.parent_father = Pedigree.objects.get(reg_no=pedigree_form['father'].value())
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
            new_pedigree_attributes.prize_winning = attributes_form['prize_winning'].value()
            new_pedigree_attributes.save()

            files = request.FILES.getlist('upload_images')
            fs = FileSystemStorage()
            for file in files:
                filename = fs.save(file.name, file)
                new_pedigree_image = PedigreeImage()
                new_pedigree_image.reg_no = Pedigree.objects.get(reg_no=new_pedigree.reg_no)
                fs.url(filename)
                new_pedigree_image.image = filename
                new_pedigree_image.save()

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


@login_required(login_url="/account/login")
@user_passes_test(is_editor)
def edit_pedigree_form(request, id):
    pedigree = Pedigree.objects.get(id__exact=int(id))

    pedigree_form = PedigreeForm(request.POST or None, request.FILES or None)
    attributes_form = AttributeForm(request.POST or None, request.FILES or None)
    image_form = ImagesForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        # check whether it's valid:
        if pedigree_form.is_valid() and attributes_form.is_valid() and image_form.is_valid():
            try:
                pedigree.breeder = Breeder.objects.get(prefix=pedigree_form['breeder'].value())
            except ObjectDoesNotExist:
                pass
            try:
                pedigree.current_owner = Breeder.objects.get(prefix=pedigree_form['current_owner'].value())
            except ObjectDoesNotExist:
                pass
            pedigree.reg_no = pedigree_form['reg_no'].value()
            pedigree.name = pedigree_form['name'].value()
            try:
                pedigree.date_of_registration = pedigree_form['date_of_registration'].value() or None
            except:
                pass
            try:
                pedigree.dob = pedigree_form['date_of_birth'].value() or None
            except:
                pass
            pedigree.sex = pedigree_form['sex'].value()
            try:
                pedigree.dod = pedigree_form['date_of_death'].value() or None
            except:
                pass
            try:
                pedigree.parent_mother = Pedigree.objects.get(reg_no=pedigree_form['mother'].value())
            except ObjectDoesNotExist:
                pass
            try:
                pedigree.parent_father = Pedigree.objects.get(reg_no=pedigree_form['father'].value())
            except ObjectDoesNotExist:
                pass
            pedigree.description = pedigree_form['description'].value()
            pedigree.note = pedigree_form['note'].value()
            pedigree.save()

            pedigree_attributes = PedigreeAttributes.objects.get(reg_no=pedigree)
            try:
                pedigree_attributes.breed = Breed.objects.get(breed_name=attributes_form['breed'].value())
            except ObjectDoesNotExist:
                pass

            eggs = attributes_form['eggs_per_week'].value()
            pedigree_attributes.eggs_per_week = int(eggs)
            pedigree_attributes.prize_winning = attributes_form['prize_winning'].value()


            files = request.FILES.getlist('upload_images')
            fs = FileSystemStorage()
            for file in files:
                filename = fs.save(file.name, file)
                new_pedigree_image = PedigreeImage()
                new_pedigree_image.reg_no = Pedigree.objects.get(reg_no=pedigree.reg_no)
                fs.url(filename)
                new_pedigree_image.image = filename
                new_pedigree_image.save()

            for image in PedigreeImage.objects.all():
                img = request.POST.get('{}-{}'.format(id, image.id))
                if img:
                    image.delete()

            pedigree.save()
            pedigree_attributes.save()

            return redirect('pedigree', pedigree.id)
    else:
        pedigree_form = PedigreeForm()

    pedigree_objs = Pedigree.objects.all()
    breeder_objs = Breeder.objects.all()
    breed_objs = Breed.objects.all()

    reg_numbers = []
    for ped in pedigree_objs:
        reg_numbers.append(str(ped.reg_no))

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

    return render(request, 'edit_pedigree_form.html', {'pedigree_form': pedigree_form,
                                                      'attributes_form': attributes_form,
                                                      'image_form': image_form,
                                                      'pedigree': pedigree})


@login_required(login_url="/account/login")
@user_passes_test(is_editor)
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
