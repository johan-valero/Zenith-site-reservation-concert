from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    avatar_user = models.ImageField(upload_to='avatar', blank=True)
    
    def __str__(self):
        affiche = f"{self.user.last_name} {self.user.first_name}"
        return affiche

class EventType(models.Model):
    name_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name_type

class HallCategory(models.Model):
    hall_category = models.CharField(max_length=50)

    def __str__(self):
        return self.hall_category

class Material(models.Model):
    category_material = models.CharField(max_length=50)

    def __str__(self):
        return self.category_material

class Artist(models.Model):
    name_artist = models.CharField(max_length=50)
    skill_artist = models.CharField(max_length=50)
    pics_artist = models.ImageField(upload_to='picsArtist', blank=True)

    def __str__(self):
        affiche = f"{self.name_artist} {self.skill_artist}"
        return affiche

class Groups(models.Model):
    name_group = models.CharField(max_length=50)
    type_group = models.CharField(max_length=50)
    artist = models.ManyToManyField(Artist)
    pics_group = models.ImageField(upload_to='picsArtist', blank=True)

    def __str__(self):
        affiche = f"{self.name_group} {self.type_group}"
        return affiche

class Events(models.Model):
    name_event = models.CharField(max_length=50)
    av_ticket = models.IntegerField(default=0)
    begin_date = models.DateTimeField("Date de debut d'event")
    end_date = models.DateTimeField("Date de fin d'event")
    description_event = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    group = models.ManyToManyField(Groups,blank=True)
    users = models.ManyToManyField(User, through='Achat', blank=True)

    def __str__(self):
        affiche = f" {self.name_event}  {self.av_ticket}"
        return affiche 

class Halls(models.Model):
    name_hall = models.CharField(max_length=50)
    size_hall = models.IntegerField(default=0)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    hall_category = models.ManyToManyField(HallCategory,blank=True)

    def __str__(self):
        affiche =f" {self.name_hall} {self.size_hall} {self.hall_category}"
        return affiche

class Contact(models.Model):
    users = models.CharField(max_length=50)
    name_contact = models.CharField(max_length=50)
    mail_contact = models.CharField(max_length=50)
    pub_date = models.DateField("Date de publication")

class Achat(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    billets_user = models.IntegerField(default=0)

    def __str__(self):
        affiche =f" {self.billets_user} {self.user}{self.event}"
        return affiche