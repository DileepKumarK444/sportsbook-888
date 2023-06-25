import json

from datetime import datetime

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt



# CRUD - EVENT

@csrf_exempt
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

        return JsonResponse({'message': 'Event created'})
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def get_all_events(request):
    try:
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def get_event(request, event_id):
    try:
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@csrf_exempt
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def delete_event(request, event_id):
    try:
        if get_event_by_id(event_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to delete a specific event by ID
                cursor.execute("DELETE FROM event WHERE id = %s", [event_id])

            return JsonResponse({'message': 'Event deleted'})
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
