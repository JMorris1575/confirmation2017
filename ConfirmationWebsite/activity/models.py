from django.db import models

# Create your models here.

class Activity(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['number']


class Page(models.Model):
    activity = models.ForeignKey(Activity)
    number = models.IntegerField()
    type = models.CharField(max_length=15,
                            choices=[('IN', 'Instructions'),
                                     ('MC', 'Multichoice'),
                                     ('ES', 'Essay'),
                                     ('AN', 'Anonymous')])
    timed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.activity) + " Page: " + str(self.number)

    class Meta:
        unique_together = ('activity', 'number')
        ordering = ['activity', 'number']
