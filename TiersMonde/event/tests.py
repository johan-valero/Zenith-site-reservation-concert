from cgitb import text
from datetime import date
from venv import create
from django.test import TestCase
from .models import Events, Achat, Users, EventType, Artist, Groups
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
# ------------------------ VERIFICATION DU REGISTER---------------------------------

def create_user(username, email, password):
    return User.objects.create_user(username, email, password) 


class UserViewsTest(TestCase):
        def test_welcome_view_with_authenticated_user(self):
            """
            view_response Test la connexion avec la page welcome 
            """
            create_user("test", "test@test", "test")
            username = "test"
            pwd = "test"
            response = self.client.post((reverse('event:welcome')), {'username': f"{username}", 'password': f"{pwd}"})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Bienvenue")


        def test_login(self):
            """
            test_login Test de connexion d'un user
            """
            response = self.client.get(reverse('event:login'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Pseudo')


        def test_registered(self):
            """
            test_registered Test d'inscription d'un user
            """
            create_user("t.test", "test@gmail", "azerty")
            response = self.client.post(reverse('event:registered'),{
                'user_name': 'test',
                'user_firstname': 'test',
                'user_email': 'test@test',
                'user_pwd': 'test',
            })
            self.assertEqual(response.status_code, 200)

# ------------------------ VERIFICATION DE l'INDEX---------------------------------

def create_type_of_event(name_type):
    typeOfEvent = EventType.objects.create(name_type=name_type)
    return typeOfEvent

def create_events(name_event, av_ticket, typeEvent):
    beginDate = timezone.now()
    endDate = beginDate + datetime.timedelta(days=7)
    return Events.objects.create(name_event=name_event, av_ticket=av_ticket, begin_date=beginDate, end_date=endDate, type=typeEvent) 

def create_artists(name_artist, skill_artist):
    pics_artist = SimpleUploadedFile(name='test_image.jpg', content=open('C:/Users/dev/Desktop/Zenith2.0/TiersMonde/event/static/event/images/picsArtist/Linkin-Park-2019-02-21-Rock.jpg', 'rb').read(), content_type='image/jpeg')
    return Artist.objects.create(name_artist=name_artist, skill_artist=skill_artist, pics_artist=pics_artist)

def create_groups(name_group, type_group):
    pics_group = SimpleUploadedFile(name='test_image.jpg', content=open('C:/Users/dev/Desktop/Zenith2.0/TiersMonde/event/static/event/images/picsArtist/Linkin-Park-2019-02-21-Rock.jpg', 'rb').read(), content_type='image/jpeg')
    return Groups.objects.create(name_group=name_group, type_group=type_group, pics_group=pics_group)


class IndexViewTest(TestCase):
    def test_index_chargement(self):
        """test_index_chargement Test du chargement de la page """
        response = self.client.get(reverse('event:index'))
        self.assertEqual(response.status_code, 200)


    def test_index_events_without_event(self):
        """ test_index_events Test sans events sur la page index"""
        response = self.client.get(reverse('event:index'))
        self.assertQuerysetEqual(response.context['event_list'], [])
        self.assertContains(response, "Pas d'évènements disponible")


    def test_index_events_by_id(self):
        """ test_index_events_by_id Test de récupération des events par l'id sur l'index"""
        typeEvent = create_type_of_event('catégorie')
        event = create_events("test", 500, typeEvent)
        url = reverse('event:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['event_list'], [event])


# ------------------------ VERIFICATION DE l'ACHAT DE BILLET ---------------------------------

class AchatBilletView(TestCase):
    def test_connected_user(self):
        """ test_index_events_by_id Test d'apparition du bouton "Acheter" en étant connecté"""
        create_user("fred", "fred@fred", "fred")
        self.client.login(username="fred", password="fred")
        typeEvent = create_type_of_event("house")
        event = create_events("test", 500, typeEvent)
        artiste = create_artists("jean", "musique")
        group = create_groups("band", "rock")
        group.artist.add(artiste)
        event.group.add(group)
        url = reverse('event:detail', args=(event.id,))
        response = self.client.get(url)
        self.assertContains(response, 'Acheter')


    def test_connected_user_buy_tickets(self):
        """ test_index_events_by_id Test d'achat de billet en étant connecté aevc des places disponibles"""
        create_user("fred", "fred@fred", "fred")
        self.client.login(username="fred", password="fred")
        typeEvent = create_type_of_event("house")
        event = create_events("test", 500, typeEvent)
        artiste = create_artists("jean", "musique")
        group = create_groups("band", "rock")
        group.artist.add(artiste)
        event.group.add(group)
        event.av_ticket -= 1
        url = reverse('event:acheter', args=(event.id,))
        response = self.client.get(url)
        self.assertEqual(event.av_ticket , 499)
        self.assertContains(response, "Votre commande a bien été pris en compte par notre site de réservation." )
        self.assertEqual(response.status_code, 200)

    def test_purchase_ticket_when_no_dispo(self):
        """ test_index_events_by_id Test d'achat de billet en étant connecté sans disponibilités de billets"""
        create_user("fred", "fred@fred", "fred")
        self.client.login(username="fred", password="fred")
        typeEvent = create_type_of_event("house")
        event = create_events("test", 0, typeEvent)
        artiste = create_artists("jean", "musique")
        group = create_groups("band", "rock")
        group.artist.add(artiste)
        event.group.add(group)
        event.av_ticket -= 1
        url = reverse('event:acheter', args=(event.id,))
        response = self.client.get(url)
        self.assertEqual(event.av_ticket , 0)
        self.assertContains(response, "Pas de places disponibles")

        def test_purchase_many_tickets(self):
            """ test_index_events_by_id Test d'achat de plusieurs tickets"""
            create_user("fred", "fred@fred", "fred")
            self.client.login(username="fred", password="fred")
            typeEvent = create_type_of_event("house")
            event = create_events("test", 500, typeEvent)
            artiste = create_artists("jean", "musique")
            group = create_groups("band", "rock")
            group.artist.add(artiste)
            event.group.add(group)
            event.av_ticket -= 5
            url = reverse('event:acheter', args=(event.id,))
            response = self.client.get(url)
            self.assertEqual(event.av_ticket , 495)

# ------------------------ VERIFICATION DE l'ANNULATION DE BILLET ---------------------------------

    # def test_cancel_tickets(self):
    #     """ test_index_events_by_id Test d'annulation de billet en étant connecté"""
    #     create_user("fred", "fred@fred", "fred")
    #     self.client.login(username="fred", password="fred")
    #     typeEvent = create_type_of_event("house")
    #     event = create_events("test", 495, typeEvent)
    #     artiste = create_artists("jean", "musique")
    #     group = create_groups("band", "rock")
    #     group.artist.add(artiste)
    #     event.group.add(group)
    #     event.av_ticket += 1
    #     url = reverse('event:annuler', args=(event.id,))
    #     response = self.client.get(url)
    #     self.assertEqual(event.av_ticket , 500)
