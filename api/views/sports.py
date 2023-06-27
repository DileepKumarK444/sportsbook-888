import json

from datetime import datetime
from django.core.cache import cache

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


# CRUD - SPORTS

@csrf_exempt
@require_http_methods(["POST"])
def create_sport(request):
    try:
        data = json.loads(request.body)
        name = data['name']
        slug = data['slug']
        active = data['active']

        if not name or not slug or active is None:
            return JsonResponse({'error': 'Invalid data. Missing required fields.'}, status=400)

        with connection.cursor() as cursor:
            # Execute raw SQL query to insert a new sport
            cursor.execute("INSERT INTO sport (name, slug, active) VALUES (%s, %s, %s)",[name, slug, active])
        cache.delete('all_sports')
        return JsonResponse({'message': 'Sport created'},status=200)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred'+str(e)}, status=500)
@require_http_methods(["GET"])
def get_all_sports(request):
    try:
        cache_key = 'all_sports'
        sports = cache.get(cache_key)
        if not sports:
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
            cache.set(cache_key, sport_list)
        else:
            # Data retrieved from cache
            sport_list = sports

        return JsonResponse({'sports': sport_list},status=200)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@require_http_methods(["GET"])
def get_sport(request, sport_id):
    try:
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
            return JsonResponse({'sport': sport_data},status=200)
        else:
            return JsonResponse({'error': 'Sport not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@csrf_exempt
@require_http_methods(["PUT"])
def update_sport(request, sport_id):
    try:
        if get_sport_by_id(sport_id):
            data = json.loads(request.body)
            name = data['name']
            slug = data['slug']
            active = data['active']
            if not name or not slug or active is None:
                return JsonResponse({'error': 'Invalid data. Missing required fields.'}, status=400)

            with connection.cursor() as cursor:
                # Execute raw SQL query to update a specific sport by ID
                cursor.execute(
                    "UPDATE sport SET name = %s, slug = %s, active = %s WHERE id = %s",
                    [name, slug, active, sport_id]
                )
            cache.delete('all_sports')
            return JsonResponse({'message': 'Sport updated'},status=200)
        else:
            return JsonResponse({'error': 'Sport not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_sport(request, sport_id):
    try:
        if get_sport_by_id(sport_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to delete a specific sport by ID
                cursor.execute("DELETE FROM sport WHERE id = %s", [sport_id])
            cache.delete('all_sports')
            return JsonResponse({'message': 'Sport deleted'},status=200)
        else:
            return JsonResponse({'error': 'Sport not found'}, status=404)
        
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def activate_sport(request):
    try:
        data = json.loads(request.body)
        active = data['active']
        sport_id = data['sport_id']
        if not sport_id or active is None:
                return JsonResponse({'error': 'Invalid data. Missing required fields.'}, status=400)

        if get_sport_by_id(sport_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to update a active field of sport by ID
                cursor.execute(
                    "UPDATE sport SET active = %s WHERE id = %s",
                    [active, sport_id]
                )

            return JsonResponse({'message': 'Sport status changed'})
        else:
            return JsonResponse({'error': 'Sport not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def get_sport_by_id(sport_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific sport by ID
        cursor.execute("SELECT * FROM sport WHERE id = %s", [sport_id])
        sport = cursor.fetchone()
    if sport:
        return True
    return False

@csrf_exempt
@require_http_methods(["POST"])
def search_sport(request):
    data = json.loads(request.body)
    name = data['name']
    active = data['active']
    threshold = data['threshold']
    with connection.cursor() as cursor:

        with connection.cursor() as cursor:
            params = []
            if threshold != '' and threshold >0:
                # query = "SELECT * FROM sport as s INNER JOIN event as e on s.id = e.sport_id WHERE e.active=true "    
                # query = '''SELECT * FROM sport as s JOIN ( 
                #         SELECT sport_id, COUNT(*) AS active_count 
                #         FROM event 
                #         WHERE active = 1 
                #         GROUP BY sport_id 
                #         ) AS event_count 
                #         ON s.id = event_count.sport_id 
                #         WHERE event_count.active_count > %s'''

                query = '''
                        SELECT s.*, COUNT(e.id) AS active_events_count
                        FROM sport AS s
                        INNER JOIN event AS e ON s.id = e.sport_id
                        WHERE e.active = 1 
                        '''
                # params.append(threshold)
            else:
                query = "SELECT * FROM sport as s WHERE 1=1"
            

            if name != '':
                query += " AND s.name REGEXP %s"
                params.append(name)

            if active != '':
                query += " AND s.active = %s"
                params.append(active)
            if threshold != '' and threshold >0:
                query += '''
                            GROUP BY s.id
                            HAVING COUNT(e.id) > %s'''
                params.append(threshold)

            cursor.execute(query, params)

            sports = cursor.fetchall()
            # print('sports',sports)
            sport_list = []
            for sport in sports:
                sport_data = {
                    'name': sport[1],
                    'slug': sport[2],
                    'active': sport[3]
                }
                sport_list.append(sport_data)
    return JsonResponse({'sports': sport_list})

    # Add more conditions as needed

    
