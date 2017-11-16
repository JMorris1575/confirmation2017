from django.db import models

# Create your models here.

class Activity(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name
