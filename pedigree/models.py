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


class Goat(models.Model):

    breeder = models.ForeignKey(Breeder, on_delete=models.PROTECT, blank=True, null=True)
    current_owner = models.ForeignKey(Breeder, on_delete=models.PROTECT, blank=True, null=True, related_name='+')
    reg_no = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    date_of_registration = models.DateField(blank=True)
    dob = models.CharField(max_length=100, blank=True)
    dod = models.CharField(max_length=100, blank=True)

    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    )

    sex = models.CharField(max_length=10, choices=GENDERS, default='Unknown')
    sire = models.CharField(max_length=100, blank=True)
    dam = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True,)
    image = models.ImageField(blank=True)

    # stats

    min_milk_yield = models.CharField(max_length=100, blank=True)
    max_milk_yield = models.CharField(max_length=100, blank=True)
    avg_milk_yield = models.CharField(max_length=100, blank=True)
    height_to_withers = models.CharField(max_length=100, blank=True)
    first_prize = models.BooleanField(default=False)
    second_prize = models.BooleanField(default=False)
    third_prize = models.BooleanField(default=False)

    def __str__(self):
        return self.reg_no