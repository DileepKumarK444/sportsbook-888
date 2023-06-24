import json
import pytz

from datetime import datetime, timezone

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from pytz import timezone


@csrf_exempt
def create_sport(request):
    data = json.loads(request.body)
    # print('data',data)
    name = data['name']
    slug = data['slug']
    active = data['active']
    with connection.cursor() as cursor:
        # Execute raw SQL query to insert a new sport
        cursor.execute("INSERT INTO sport (name, slug, active) VALUES (%s, %s, %s)",[name, slug, active])

    return JsonResponse({'message': 'Sport created'})

def get_all_sports(request):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch all sports
        cursor.execute("SELECT * FROM sport")
        sports = cursor.fetchall()

    sport_list = []
    for sport in sports:
        sport_data = {
            'id':sport[0],
            'name': sport[1],
            'slug': sport[2],
            'active': sport[3]
        }
        sport_list.append(sport_data)

    return JsonResponse({'sports': sport_list})

def get_sport(request, sport_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific sport by ID
        cursor.execute("SELECT * FROM sport WHERE id = %s", [sport_id])
        sport = cursor.fetchone()

    if sport:
        sport_data = {
            'id' : sport_id,
            'name': sport[1],
            'slug': sport[2],
            'active': sport[3]
        }
        return JsonResponse({'sport': sport_data})
    else:
        return JsonResponse({'error': 'Sport not found'}, status=404)
@csrf_exempt
def update_sport(request, sport_id):
    if get_sport_by_id(sport_id):
        data = json.loads(request.body)
        name = data['name']
        slug = data['slug']
        active = data['active']

        with connection.cursor() as cursor:
            # Execute raw SQL query to update a specific sport by ID
            cursor.execute(
                "UPDATE sport SET name = %s, slug = %s, active = %s WHERE id = %s",
                [name, slug, active, sport_id]
            )

        return JsonResponse({'message': 'Sport updated'})
    else:
        return JsonResponse({'error': 'Sport not found'}, status=404)
@csrf_exempt
def delete_sport(request, sport_id):
    if get_sport_by_id(sport_id):
        with connection.cursor() as cursor:
            # Execute raw SQL query to delete a specific sport by ID
            cursor.execute("DELETE FROM sport WHERE id = %s", [sport_id])

        return JsonResponse({'message': 'Sport deleted'})
    else:
        return JsonResponse({'error': 'Sport not found'}, status=404)

def get_sport_by_id(sport_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific sport by ID
        cursor.execute("SELECT * FROM sport WHERE id = %s", [sport_id])
        sport = cursor.fetchone()
    if sport:
        return True
    return False

#EVENT

@csrf_exempt
def create_event(request):
    data = json.loads(request.body)
    name = data['name']
    slug = data['slug']
    active = data['active']
    event_type = data['type']
    sport_id = data['sport_id']
    status = 'Pending'
    scheduled_start= datetime.utcnow()

    with connection.cursor() as cursor:
        # Execute raw SQL query to insert a new event
        cursor.execute(
            "INSERT INTO event (name, slug, active, type, sport_id, status, scheduled_start) "
            "VALUES (%s, %s, %s, %s, %s,%s,%s)",
            [name, slug, active, event_type, sport_id,status,scheduled_start]
        )

    return JsonResponse({'message': 'Event created'})

def get_all_events(request):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch all events
        cursor.execute("SELECT * FROM event")
        events = cursor.fetchall()

    event_list = []
    for event in events:
        event_data = {
            'id': event[0],
            'name': event[1],
            'slug': event[2],
            'active': event[3],
            'type': event[4],
            'sport_id': event[7],
            'status' : event[5],
            'scheduled_start' : event[8],
            'actual_start' : event[6],
        }
        event_list.append(event_data)

    return JsonResponse({'events': event_list})

def get_event(request, event_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific event by ID
        cursor.execute("SELECT * FROM event WHERE id = %s", [event_id])
        event = cursor.fetchone()

    if event:
        event_data = {
            'id':event_id,
            'name': event[1],
            'slug': event[2],
            'active': event[3],
            'type': event[4],
            'sport_id': event[5]
        }
        return JsonResponse({'event': event_data})
    else:
        return JsonResponse({'error': 'Event not found'}, status=404)
@csrf_exempt
def update_event(request, event_id):
    if get_event_by_id(event_id):
        data = json.loads(request.body)
        name = data['name']
        slug = data['slug']
        active = data['active']
        event_type = data['type']
        sport_id = str(data['sport_id'])
        status = data['status']
        # scheduled_start = data['scheduled_start']
        

        with connection.cursor() as cursor:
            # Execute raw SQL query to update a specific event by ID
            cursor.execute(
                "UPDATE event SET name = %s, slug = %s, active = %s, "
                "type = %s, sport_id = %s, status = %s WHERE id = %s",
                [name, slug, active, event_type, sport_id,status, event_id]
            )
        
        if status == 'Started':
            with connection.cursor() as cursor:
            # Execute raw SQL query to update a actual_start if status is Started
                cursor.execute(
                    "UPDATE event SET actual_start = %s WHERE id = %s",
                    [datetime.utcnow(), event_id]
                )

        # Check if all selections for the event are inactive
        if active == False:

            # Check if all events for the sport are inactive
            with connection.cursor() as cursor:
                # Execute raw SQL query to check if all events of the sport are inactive
                cursor.execute(
                    "SELECT COUNT(*) FROM event WHERE sport_id = %s AND active = %s",
                    [sport_id, True]
                )
                result = cursor.fetchone()

                if result[0] == 0:
                    # All events are inactive, update sport's active status
                    cursor.execute(
                        "UPDATE sport SET active = %s WHERE id = %s",
                        [False, sport_id]
                    )
                    
            

        return JsonResponse({'message': 'Event updated'})
    else:
        return JsonResponse({'error': 'Event not found'}, status=404)

def delete_event(request, event_id):
    if get_event_by_id(event_id):
        with connection.cursor() as cursor:
            # Execute raw SQL query to delete a specific event by ID
            cursor.execute("DELETE FROM event WHERE id = %s", [event_id])

        return JsonResponse({'message': 'Event deleted'})
    else:
        return JsonResponse({'error': 'Event not found'}, status=404)


def get_event_by_id(event_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific event by ID
        cursor.execute("SELECT * FROM event WHERE id = %s", [event_id])
        event = cursor.fetchone()

    if event:
        return True
    return False

#SELECTION

@csrf_exempt
def create_selection(request):
    data = json.loads(request.body)
    name = data['name']
    event_id = data['event_id']
    price = data['price']
    active = data['active']
    outcome = data['outcome']

    with connection.cursor() as cursor:
        # Execute raw SQL query to insert a new selection
        cursor.execute(
            "INSERT INTO selection (name, event_id, price, active, outcome) "
            "VALUES (%s, %s, %s, %s, %s)",
            [name, event_id, price, active, outcome]
        )

    return JsonResponse({'message': 'Selection created'})

def get_all_selections(request):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch all selections
        cursor.execute("SELECT * FROM selection")
        selections = cursor.fetchall()

    selection_list = []
    for selection in selections:
        selection_data = {
            'id': selection[0],
            'name': selection[1],
            'event_id': selection[2],
            'price': selection[3],
            'active': selection[4],
            'outcome': selection[5]
        }
        selection_list.append(selection_data)

    return JsonResponse({'selections': selection_list})

def get_selection(request, selection_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific selection by ID
        cursor.execute("SELECT * FROM selection WHERE id = %s", [selection_id])
        selection = cursor.fetchone()

    if selection:
        selection_data = {
            'id': selection_id,
            'name': selection[1],
            'event_id': selection[2],
            'price': selection[3],
            'active': selection[4],
            'outcome': selection[5]
        }
        return JsonResponse({'selection': selection_data})
    else:
        return JsonResponse({'error': 'Selection not found'}, status=404)
@csrf_exempt
def update_selection(request, selection_id):
    if get_selection_by_id(selection_id):
        data = json.loads(request.body)
        name = data['name']
        event_id = data['event_id']
        price = data['price']
        active = data['active']
        outcome = data['outcome']

        with connection.cursor() as cursor:
            # Execute raw SQL query to update a specific selection by ID
            cursor.execute(
                "UPDATE selection SET name = %s, event_id = %s, price = %s, "
                "active = %s, outcome = %s WHERE id = %s",
                [name, event_id, price, active, outcome, selection_id]
            )

        if active == False:
            with connection.cursor() as cursor:
                # Execute raw SQL query to check if all selections are inactive
                cursor.execute(
                    "SELECT COUNT(*) FROM selection WHERE event_id = %s AND active = %s",
                    [event_id, True]
                )
                result = cursor.fetchone()

                if result[0] == 0:
                    # All selections are inactive, update event's active status
                    cursor.execute(
                        "UPDATE event SET active = %s WHERE id = %s",
                        [False, event_id]
                    )

        return JsonResponse({'message': 'Selection updated'})
    else:
        return JsonResponse({'error': 'Selection not found'}, status=404)

def delete_selection(request, selection_id):
    if get_selection_by_id(selection_id):
        with connection.cursor() as cursor:
            # Execute raw SQL query to delete a specific selection by ID
            cursor.execute("DELETE FROM selection WHERE id = %s", [selection_id])

        return JsonResponse({'message': 'Selection deleted'})
    else:
        return JsonResponse({'error': 'Selection not found'}, status=404)

def get_selection_by_id(selection_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific selection by ID
        cursor.execute("SELECT * FROM selection WHERE id = %s", [selection_id])
        selection = cursor.fetchone()

    if selection:
        return True
    return False


def sports_with_name_regex(request, regex):

    with connection.cursor() as cursor:

        with connection.cursor() as cursor:
            # Execute raw SQL query to fetch sports with names matching the regex pattern
            cursor.execute("SELECT * FROM sport WHERE name REGEXP %s", [regex])
            sports = cursor.fetchall()
            sport_list = []
            for sport in sports:
                sport_data = {
                    'name': sport[1],
                    'slug': sport[2],
                    'active': sport[3]
                }
                sport_list.append(sport_data)

            # Execute raw SQL query to fetch events with names matching the regex pattern
            cursor.execute("SELECT * FROM event WHERE name REGEXP %s", [regex])
            events = cursor.fetchall()
            event_list = []
            for event in events:
                event_data = {
                    'name': event[1],
                    'slug': event[2],
                    'active': event[3],
                    'type' : event[4],
                    'sport' : event[7],
                    'status' : event[5],
                    'scheduled_start' : event[8],
                    'actual_start' : event[6]
                }
                event_list.append(event_data)

            # Execute raw SQL query to fetch selections with names matching the regex pattern
            cursor.execute("SELECT * FROM selection WHERE name REGEXP %s", [regex])
            selections = cursor.fetchall()

            selection_list = []
            for selection in selections:
                selection_data = {
                    'name': selection[1],
                    'event': selection[5],
                    'price': selection[2],
                    'active' : selection[3],
                    'outcome' : selection[4],
                }
                selection_list.append(selection_data)

        
    return JsonResponse({'sports': sport_list,'events':event_list,'selections':selection_list})


def events_with_active_threshold(request, threshold):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch events with minimum number of active selections higher than threshold
        cursor.execute("""
            SELECT event.* 
            FROM event AS event 
            JOIN (
                SELECT event_id, COUNT(*) AS active_count 
                FROM selection 
                WHERE active = 1 
                GROUP BY event_id
            ) AS selection_count 
            ON event.id = selection_count.event_id 
            WHERE selection_count.active_count > %s
        """, [threshold])
        events = cursor.fetchall()

    event_list = []
    for event in events:
        event_data = {
            'name': event[1],
            'slug': event[2],
            'active': event[3],
            'type': event[4],
            'sport_id': event[5],
            'status': event[6],
            'scheduled_start': event[7],
            'actual_start': event[8]
        }
        event_list.append(event_data)

    return JsonResponse({'events': event_list})
# @csrf_exempt    
# def events_in_timeframe(request):
#     # Define the timezone
#     data = json.loads(request.body)
#     # timezone = data['timezone']
#     start_time = data['start_time']
#     end_time = data['end_time']
#     tz = timezone("Asia/Kolkata")

@csrf_exempt    
def events_in_timeframe(request):

    data = json.loads(request.body)
    timezone = data['timezone']
    start_time = data['start_time']
    end_time = data['end_time']
    # tz = timezone("Asia/Kolkata")
    tz = pytz.timezone(timezone)  # Get the timezone object based on the provided timezone name

    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch events scheduled to start in a specific timeframe for a specific timezone
        cursor.execute("""
            SELECT * 
            FROM event 
            WHERE scheduled_start >= %s 
            AND scheduled_start <= %s
        """, [start_time, end_time])
        events = cursor.fetchall()

    event_list = []
    for event in events:
        # scheduled_start = event[8].isoformat() if event[8] else None
        # actual_start = event[6].isoformat() if event[6] else None
        
        scheduled_start_utc = event[8]  
        scheduled_start_local = scheduled_start_utc.astimezone(tz) if scheduled_start_utc else None
        
        actual_start_utc = event[6]  
        actual_start_local = actual_start_utc.astimezone(tz) if actual_start_utc else None

        # scheduled_start = event[8]
        # actual_start = event[6]

        event_data = {
            'name': event[1],
            'slug': event[2],
            'active': event[3],
            'type': event[4],
            'sport_id': event[7],
            'status': event[5],
            'scheduled_start1': event[8],
            'actual_start1': event[6],
            'scheduled_start': scheduled_start_local.isoformat() if scheduled_start_local else None,
            'actual_start': actual_start_local.isoformat() if actual_start_local else None
        }
        event_list.append(event_data)

    return JsonResponse({'events': event_list})