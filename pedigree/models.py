from django.db import models
from breeder.models import Breeder
from breed.models import Breed

class Pedigree(models.Model):
    breeder = models.ForeignKey(Breeder, on_delete=models.CASCADE, blank=True, null=True)
    current_owner = models.ForeignKey(Breeder, on_delete=models.CASCADE, blank=True, null=True, related_name='owner')
    reg_no = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    date_of_registration = models.DateField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)

    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    sex = models.CharField(max_length=10, choices=GENDERS, default=None, null=True)
    parent_father = models.ForeignKey('self', related_name='farther', on_delete=models.CASCADE, blank=True, null=True)
    parent_mother = models.ForeignKey('self', related_name='mother', on_delete=models.CASCADE, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True)

    # hidden
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reg_no


class PedigreeImage(models.Model):
    reg_no = models.ForeignKey(Pedigree, related_name='images', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.reg_no)


class PedigreeAttributes(models.Model):
    reg_no = models.OneToOneField(Pedigree, on_delete=models.CASCADE, primary_key=True, related_name='attribute')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, blank=True, null=True, related_name='breed')
    eggs_per_week = models.IntegerField(default=0)
    prize_winning = models.BooleanField(default=False)

    def __str__(self):
        return str(self.reg_no)

