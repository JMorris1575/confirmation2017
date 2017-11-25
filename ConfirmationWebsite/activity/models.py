from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Activity(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    overview = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['number']


class Action(models.Model):
    activity = models.ForeignKey(Activity)
    number = models.IntegerField()
    type = models.CharField(max_length=15,
                            choices=[('IN', 'Instructions'),
                                     ('MC', 'Multichoice'),
                                     ('ES', 'Essay'),
                                     ('AN', 'Anonymous'),
                                     ('CO', 'Table of Contents')])
    text = models.TextField(default="")
    timed = models.BooleanField(default=False)


    class Meta:
        unique_together = ('activity', 'number')
        ordering = ['activity', 'number']

    def __str__(self):
        count = len(Action.objects.filter(activity=self.activity))
        return str(self.activity) + " - Number " + str(self.number)

    def get_absolute_url(self):
        number = self.number
        slug = self.activity.slug
        return '/activity/' + slug + '/' + str(number) +'/'

    def previous(self):
        number = self.number
        slug = self.activity.slug
        if number == 1:
            return '/activity/' + slug + '/'
        else:
            return '/activity/' + slug + '/' + str(number - 1) + '/'

    def next(self):
        number = self.number
        max = len(Action.objects.filter(activity=self.activity))
        slug = self.activity.slug
        if number == max:
            return '/activity/' + slug + '/congrats/'
        else:
            return '/activity/' + slug + '/' + str(number + 1) + '/'


class UserResponse(models.Model):
    user = models.ForeignKey(User)
    action = models.ForeignKey(Action)
    #response = models.ForeignKey(Response)
    essay = models.TextField()

    def __str__(self):
        return self.user.username + "'s response to " + str(self.action)
