from django.db import models


class Breeder(models.Model):

    prefix = models.CharField(max_length=100, blank=True)
    contact_name = models.CharField(max_length=100, blank=True)

    address = models.CharField(max_length=250, blank=True)
    phone_number1 = models.CharField(max_length=100, blank=True)
    phone_number2 = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)

    active = models.BooleanField(default=False)

    def __str__(self):
        return self.prefix


class Pedigree(models.Model):

    breeder = models.ForeignKey(Breeder, on_delete=models.PROTECT, blank=True, null=True)
    current_owner = models.ForeignKey(Breeder, on_delete=models.PROTECT, blank=True, null=True, related_name='+')
    reg_no = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    date_of_registration = models.DateField(blank=True)
    dob = models.DateField(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)

    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    )

    sex = models.CharField(max_length=10, choices=GENDERS, default='Unknown')
    parent_father = models.ForeignKey('self', related_name='farther', on_delete=models.CASCADE, blank=True, null=True)
    parent_mother = models.ForeignKey('self', related_name='mother', on_delete=models.CASCADE, blank=True, null=True)
    notes = models.TextField(blank=True,)
    image = models.ImageField(blank=True)

    # stats

    def __str__(self):
        return self.reg_no


# class PedigreeAtributes(models.Model):
