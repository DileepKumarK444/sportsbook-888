import json
import pytz

from datetime import datetime
from django.core.cache import cache

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods



# CRUD - EVENT

@csrf_exempt
@require_http_methods(["POST"])
def create_event(request):
    try:
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
        cache.delete('all_events')
        return JsonResponse({'message': 'Event created'})
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

@require_http_methods(["GET"])
def get_all_events(request):
    try:
        cache_key = 'all_events'
        events = cache.get(cache_key)
        if not events:
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
            cache.set(cache_key, event_list)
        else:
            # Data retrieved from cache
            event_list = events

        return JsonResponse({'events': event_list})
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

@require_http_methods(["GET"])
def get_event(request, event_id):
    try:
        with connection.cursor() as cursor:
            # Execute raw SQL query to fetch a specific event by ID
            cursor.execute("SELECT * FROM event WHERE id = %s", [event_id])
            event = cursor.fetchone()

        if event:
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
            return JsonResponse({'event': event_data})
        else:
            return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_event(request, event_id):
    try:
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
            check_event_active(sport_id)
            cache.delete('all_events')
            return JsonResponse({'message': 'Event updated'})
        else:
            return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_event(request, event_id):
    try:
        if get_event_by_id(event_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to delete a specific event by ID
                cursor.execute("DELETE FROM event WHERE id = %s", [event_id])
            cache.delete('all_events')
            return JsonResponse({'message': 'Event deleted'})
        else:
            return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)


def check_event_active(sport_id):
    # if active == False:
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
        else:
            cursor.execute(
                "UPDATE sport SET active = %s WHERE id = %s",
                [True, sport_id]
            )
    return True

@csrf_exempt
@require_http_methods(["PUT"])
def activate_event(request):
    try:
        data = json.loads(request.body)
        active = data['active']
        event_id = data['event_id']
        sport_id = data['sport_id']
        if get_event_by_id(event_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to update a active field of event by ID
                cursor.execute(
                    "UPDATE event SET active = %s WHERE id = %s",
                    [active, event_id]
                )
            # if active == False:
            check_event_active(sport_id)

            return JsonResponse({'message': 'Event status changed'})
        else:
            return JsonResponse({'error': 'Event not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def get_event_by_id(event_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific event by ID
        cursor.execute("SELECT * FROM event WHERE id = %s", [event_id])
        event = cursor.fetchone()

    if event:
        return True
    return False

@csrf_exempt
@require_http_methods(["POST"])
def search_event(request):
    data = json.loads(request.body)
    name = data['name']
    active = data['active']
    status = data['status']
    threshold = data['threshold']

    timezone = data['timezone']

    # convert local time to UTC
    start_time = ''
    end_time = ''
    if data['start_time'] != '' and data['end_time'] !='':
        start_time = local_to_utc(data['start_time'],timezone)
        end_time = local_to_utc(data['end_time'],timezone)

    # print(start_time)


    with connection.cursor() as cursor:

        with connection.cursor() as cursor:
            params = []
            if threshold != '' and threshold >0:
                # query = "SELECT * FROM event as e INNER JOIN selection as s on e.id = s.event_id WHERE s.active=true "    
                # query = '''SELECT * FROM event as e JOIN ( 
                #         SELECT event_id, COUNT(*) AS active_count 
                #         FROM selection 
                #         WHERE active = 1 
                #         GROUP BY event_id 
                #         ) AS selection_count 
                #         ON e.id = selection_count.event_id 
                #         WHERE selection_count.active_count > %s '''
                # params.append(threshold)
                query = '''
                        SELECT e.*, COUNT(s.id) AS active_selection_count
                        FROM event AS e
                        INNER JOIN selection AS s ON e.id = s.event_id
                        WHERE s.active = 1
                '''
            else:
                query = "SELECT * FROM event as e WHERE 1=1"
            

            if name != '':
                query += " AND e.name REGEXP %s"
                params.append(name)

            if active != '':
                query += " AND e.active = %s"
                params.append(active)
            
            if status != '':
                query += " AND e.status = %s"
                params.append(status)

            if start_time !='' and end_time !='':
                query += " AND scheduled_start >= %s AND scheduled_start <= %s"
                params.append(start_time)
                params.append(end_time)
            
            if threshold != '' and threshold >0:
                query += '''
                        GROUP BY e.id
                        HAVING COUNT(s.id) > %s
                        '''
                params.append(threshold)

            cursor.execute(query, params)

            events = cursor.fetchall()
            event_list = []
            for event in events:
                scheduled_start = ''
                actual_start = ''

                if event[8] != None and timezone != '':
                    scheduled_start = utc_to_local(event[8],timezone)
                if event[6] != None and timezone != '':
                    actual_star = utc_to_local(event[6],timezone)
                event_data = {
                    'id': event[0],
                    'name': event[1],
                    'slug': event[2],
                    'active': event[3],
                    'type': event[4],
                    'sport_id': event[7],
                    'status' : event[5],
                    'scheduled_start' : scheduled_start,
                    'actual_start' : actual_start,
                }
                event_list.append(event_data)
    return JsonResponse({'events': event_list})

def local_to_utc(dt,tz):

    formatted_datetime = dt

    given_datetime = datetime.strptime(formatted_datetime, '%Y-%m-%d %H:%M:%S')

    given_timezone = pytz.timezone(tz)

    localized_datetime = given_timezone.localize(given_datetime)

    utc_datetime = localized_datetime.astimezone(pytz.UTC)

    formatted_datetime = utc_datetime.strftime('%Y-%m-%d %H:%M:%S %Z%z')

    return formatted_datetime

def utc_to_local(dt,tz):

    dt = datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S.%f")

    utc_timezone = pytz.UTC
    utc_dt = dt.replace(tzinfo=utc_timezone)

    local_timezone = pytz.timezone(tz)

    local_datetime = utc_dt.astimezone(local_timezone)

    return local_datetime