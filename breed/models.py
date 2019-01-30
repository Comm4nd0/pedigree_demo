from django.db import models


class Breed(models.Model):
    breed_name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.breed_name
