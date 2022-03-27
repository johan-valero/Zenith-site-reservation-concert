from django.contrib import admin
from .models import Artist, EventType, Events, HallCategory, Halls, Material, Users, Groups, Contact, Achat

# Register your models here.
admin.site.register(Users)
admin.site.register(EventType)
admin.site.register(HallCategory)
admin.site.register(Material)
admin.site.register(Artist)
admin.site.register(Groups)
admin.site.register(Events)
admin.site.register(Halls)
admin.site.register(Contact)
admin.site.register(Achat)