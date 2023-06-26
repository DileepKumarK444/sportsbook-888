from django.test import TestCase, Client
from django.urls import reverse
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
        self.assertEqual(response.status_code, 200)
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
    