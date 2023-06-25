import json
import pytz

from datetime import datetime

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
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

@require_http_methods(["GET"])
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
@require_http_methods(["POST"])
def events_in_timeframe(request):

    data = json.loads(request.body)
    timezone = data['timezone']
    start_time = data['start_time']
    end_time = data['end_time']
    # tz = timezone("Asia/Kolkata")
    tz = pytz.timezone(timezone) 

    with connection.cursor() as cursor:
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