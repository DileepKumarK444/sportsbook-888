import json

from datetime import datetime

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt


# CRUD - SPORTS

@csrf_exempt
def create_sport(request):
    try:
        data = json.loads(request.body)
        # print('data',data)
        name = data['name']
        slug = data['slug']
        active = data['active']
        with connection.cursor() as cursor:
            # Execute raw SQL query to insert a new sport
            cursor.execute("INSERT INTO sport (name, slug, active) VALUES (%s, %s, %s)",[name, slug, active])

        return JsonResponse({'message': 'Sport created'})
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred'+str(e)}, status=500)

def get_all_sports(request):
    try:
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

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
            return JsonResponse({'sport': sport_data})
        else:
            return JsonResponse({'error': 'Sport not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@csrf_exempt
def update_sport(request, sport_id):
    try:
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@csrf_exempt
def delete_sport(request, sport_id):
    try:
        if get_sport_by_id(sport_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to delete a specific sport by ID
                cursor.execute("DELETE FROM sport WHERE id = %s", [sport_id])

            return JsonResponse({'message': 'Sport deleted'})
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
