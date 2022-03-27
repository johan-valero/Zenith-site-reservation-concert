from unicodedata import name
from django.urls import path
from . import views

app_name = 'event'
urlpatterns = [
    path('', views.index, name='index'),
    path('liste', views.liste, name='liste'),
    path('<int:event_id>/detail/', views.detail, name='detail'),
    path('informations/', views.informations, name='informations'),
    path('register/', views.register, name='register'),
    path('registered/', views.registered, name='registered'),
    path('welcome/', views.welcome, name='welcome'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('password/', views.new_password, name='password'),
    path('contact/', views.contact, name='contact'),
    path('<int:event_id>/detail/acheter/', views.acheter, name='acheter'),
    path('faq/', views.faq, name='faq'),
    path('profil/', views.profil, name='profil'),
    path('profil/annuler/<int:event_id>', views.annuler, name='annuler'),
    # path('<int:event_id>/detail/reserver/', views.reserver, name='reserver'),
]