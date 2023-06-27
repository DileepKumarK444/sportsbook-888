from django.test import TestCase, Client
from django.urls import reverse
from .models import Sport, Event,Selection
from django.utils import timezone

import json

class SportAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_sport()

    def create_sport(self):
        url = reverse('create_sport')
        data = {
            'name': 'Football',
            'slug': 'football',
            'active': True
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Sport created'})

    def test_get_all_sports(self):
        url = reverse('get_all_sports')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        

    def test_get_sport(self):
        sport_id = 1 
        url = reverse('get_sport', args=[sport_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        

    def test_update_sport(self):
        sport_id = 1  
        url = reverse('update_sport', args=[sport_id])
        data = {
            'name': 'Updated Sport',
            'slug': 'updated-sport',
            'active': False
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Sport updated'})

    def test_delete_sport(self):
        sport_id = 1 
        url = reverse('delete_sport', args=[sport_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Sport deleted'})


class EventAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_sport(self):
        url = reverse('create_sport')
        data = {
            'id': 1,
            'name': 'Football',
            'slug': 'football',
            'active': True
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Sport created'})

    def test_create_event(self):
        # First, create the sport record
        self.test_create_sport()

        url = reverse('create_event')
        data = {
            'name': 'Event 1',
            'slug': 'event-1',
            'active': True,
            'type': 'Type 1',
            'sport_id': 1,
            'status': 'Started',
            'scheduled_start': '2023-06-15T10:00:00Z',
            'actual_start': '2023-06-15T10:05:00Z'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Event created'})

    def test_get_all_events(self):
        url = reverse('get_all_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert the response contains the expected events data

    def test_get_event(self):
        self.test_create_event()
        event_id = 1
        url = reverse('get_event', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert the response contains the expected event data
        

    def test_update_event(self):
        self.test_create_event()
        event_id = 1
        url = reverse('update_event', args=[event_id])
        data = {
            'name': 'Updated Event',
            'slug': 'updated-event',
            'active': False,
            'type': 'Type 2',
            'sport_id': 1,
            'status': 'Started',
            'scheduled_start': '2023-06-15T10:00:00Z',
            'actual_start': '2023-06-15T10:05:00Z'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Event updated'})

    def test_delete_event(self):

        self.test_create_event()
        event_id = 1
        url = reverse('delete_event', args=[event_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Event deleted'})

class SelectionAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_sport(self):
        url = reverse('create_sport')
        data = {
            'id': 1,
            'name': 'Football',
            'slug': 'football',
            'active': True
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Sport created'})
    def test_create_event(self):
        # First, create the sport record
        self.test_create_sport()

        url = reverse('create_event')
        data = {
            'name': 'Event 1',
            'slug': 'event-1',
            'active': True,
            'type': 'Type 1',
            'sport_id': 1,
            'status': 'Started',
            'scheduled_start': '2023-06-15T10:00:00Z',
            'actual_start': '2023-06-15T10:05:00Z'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Event created'})

    def test_create_selection(self):
        # First, create the sport record
        self.test_create_event()

        url = reverse('create_selection')
        data = {
            'name': 'Selection 1',
            'event_id': 1,
            'price' : 12.0,
            'active': True,
            'outcome': 'Outcome 1'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Selection created'})

    def test_get_all_selections(self):
        url = reverse('get_all_selections')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert the response contains the expected events data

    def test_get_selection(self):
        self.test_create_selection()
        selection_id = 1
        url = reverse('get_selection', args=[selection_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert the response contains the expected event data

       
        

    def test_update_selection(self):
        self.test_create_selection()
        selection_id = 1
        url = reverse('update_selection', args=[selection_id])
        data = {
            'name': 'Updated Selection',
            'event_id': 1,
            'sport_id' : 1,
            'price' : 12.0,
            'active': True,
            'outcome': 'Outcome 1'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Selection updated'})

    def test_delete_selection(self):

        self.test_create_selection()
        selection_id = 1
        url = reverse('delete_selection', args=[selection_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Selection deleted'})


class SportAndEventTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_sport(self):
        url = reverse('create_sport')
        data = {
            'name': 'Football',
            'slug': 'football',
            'active': True
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Sport created'})

    def test_create_event(self):
        # First, create the sport record
        self.test_create_sport()

        url = reverse('create_event')
        data = {
            'name': 'Event 1',
            'slug': 'event-1',
            'active': True,
            'type': 'Type 1',
            'sport_id': 1,
            'status': 'Started',
            'scheduled_start': '2023-06-15T10:00:00Z',
            'actual_start': '2023-06-15T10:05:00Z'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Event created'})
    

class SportSearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search_sport')
        sport1 = Sport.objects.create(name='Football', slug='football', active=True)
        sport2 = Sport.objects.create(name='Basketball', slug='basketball', active=True)
        event1 = Event.objects.create(name='Event 1', slug='event-1', active=True, type='Type 1', sport=sport1, status='Started')
        event2 = Event.objects.create(name='Event 2', slug='event-2', active=True, type='Type 2', sport=sport2, status='Started')
        event3 = Event.objects.create(name='Event 3', slug='event-3', active=False, type='Type 3', sport=sport1, status='Ended')

    def test_search_sport_with_threshold(self):
        # Make a request to the view
        data = {
            'name': '',
            'active': '',
            'threshold': 0
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        # Verify the response
        print('response',response.content)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'sports': [
                {'name': 'Football', 'slug': 'football', 'active': True},
                {'name': 'Basketball', 'slug': 'basketball', 'active': True},
            ]
        }
        self.assertEqual(json.loads(response.content.decode('utf-8')), expected_data)

    def test_search_sport_without_threshold(self):
        
        # Make a request to the view
        data = {
            'name': '',
            'active': '',
            'threshold': ''
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        # Verify the response
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'sports': [
                {'name': 'Football', 'slug': 'football', 'active': True},
                {'name': 'Basketball', 'slug': 'basketball', 'active': True},
            ]
        }
        self.assertEqual(json.loads(response.content.decode('utf-8')), expected_data)


class SearchEventTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('search_event')
        sport = Sport.objects.create(name='Football', slug='football', active=True)

        # Create Event instances and save them to the database
        event1 = Event.objects.create(
            name='Event 1',
            slug='event-1',
            active=True,
            type='Type 1',
            sport=sport,
            status='Started',
            scheduled_start=timezone.now(),
            actual_start=timezone.now()
        )

        event2 = Event.objects.create(
            name='Event 2',
            slug='event-2',
            active=True,
            type='Type 2',
            sport=sport,
            status='Pending',
            scheduled_start=timezone.now(),
            actual_start=None
        )

    def test_search_event(self):

        data = {
            'name': 'Event',
            'active': True,
            'status': '',
            'threshold': '',
            'timezone': 'America/New_York',
            'start_time': '2023-06-15 10:00:00',
            'end_time': '2023-06-27 18:00:00'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        event_list = response.json().get('events')
        self.assertIsNotNone(event_list)
        self.assertGreater(len(event_list), 0)
        # Add more assertions to validate the returned event data
        self.assertEqual(event_list[0]['name'], 'Event 1')

    def test_search_event_with_empty_parameters(self):


        data = {
            'name': '',
            'active': '',
            'status': '',
            'threshold': '',
            'timezone': 'Asia/Kolkata',
            'start_time': '',
            'end_time': ''
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        event_list = response.json().get('events')
        self.assertIsNotNone(event_list)
        self.assertEqual(len(event_list), 2)



class SearchSelectionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Insert sample data into the database for testing
        self.url = reverse('search_selection')
        sport = Sport.objects.create(name='Football', slug='football', active=True)
        event = Event.objects.create(
            name='Match 1',
            slug='match-1',
            active=True,
            type='Football Match',
            sport=sport,
            status='Pending',
            scheduled_start='2023-06-15T10:00:00Z',
            actual_start=None
        )
        selection = Selection.objects.create(
            name='Selection 1',
            event=event,
            price=1.5,
            active=True,
            outcome='Win'
        )
    
    def test_search_selection(self):
        data = {
            'name': 'Selection 1',
            'active': 'true',
            'outcome': 'Win',
            'price_from': '1.0',
            'price_to': '2.0',
            'price_condtion': 'bw'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)