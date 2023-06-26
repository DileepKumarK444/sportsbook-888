import json

from datetime import datetime
from django.core.cache import cache

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# CRUD - SELECTION

@csrf_exempt
@require_http_methods(["POST"])
def create_selection(request):
    try:
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

@require_http_methods(["GET"])
def get_all_selections(request):
    try:
        cache_key = 'all_selections'
        selections = cache.get(cache_key)
        if not selections:
            with connection.cursor() as cursor:
                # Execute raw SQL query to fetch all selections
                cursor.execute("SELECT * FROM selection as s "
                                "INNER JOIN event e on e.id = s.event_id "
                                )
                selections = cursor.fetchall()
            selection_list = []
            for selection in selections:
                selection_data = {
                    'id': selection[0],
                    'name': selection[1],
                    'event_id': selection[5],
                    'price': selection[2],
                    'active': selection[3],
                    'outcome': selection[4],
                    'sport_id': selection[13]
                }
                selection_list.append(selection_data)
            cache.set(cache_key, selection_list)
        else:
            # Data retrieved from cache
            selection_list = selections

        return JsonResponse({'selections': selection_list})
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

@require_http_methods(["GET"])
def get_selection(request, selection_id):
    try:
        with connection.cursor() as cursor:
            # Execute raw SQL query to fetch a specific selection by ID
            cursor.execute(
                "SELECT * FROM selection as s "
                "INNER JOIN event e on e.id = s.event_id WHERE s.id = %s", [selection_id])
            selection = cursor.fetchone()

        if selection:
            selection_data = {
                'id': selection[0],
                'name': selection[1],
                'event_id': selection[5],
                'price': selection[2],
                'active': selection[3],
                'outcome': selection[4],
                'sport_id': selection[13]
            }
            return JsonResponse({'selection': selection_data})
        else:
            return JsonResponse({'error': 'Selection not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_selection(request, selection_id):
    try:
        if get_selection_by_id(selection_id):
            data = json.loads(request.body)
            name = data['name']
            event_id = data['event_id']
            sport_id = data['sport_id']
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

            # if active == False:
            check_selection_active(event_id,sport_id)
            cache.delete('all_selections')
            return JsonResponse({'message': 'Selection updated'})
        else:
            return JsonResponse({'error': 'Selection not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_selection(request, selection_id):
    try:
        if get_selection_by_id(selection_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to delete a specific selection by ID
                cursor.execute("DELETE FROM selection WHERE id = %s", [selection_id])
            cache.delete('all_selections')
            return JsonResponse({'message': 'Selection deleted'})
        else:
            return JsonResponse({'error': 'Selection not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)



@csrf_exempt
@require_http_methods(["PUT"])
def activate_selection(request):
    try:
        data = json.loads(request.body)
        active = data['active']
        sport_id = data['sport_id']
        event_id = data['event_id']
        selection_id = data['selection_id']
        if get_selection_by_id(selection_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to update a active field of selection by ID
                cursor.execute(
                    "UPDATE selection SET active = %s WHERE id = %s",
                    [active, selection_id]
                )
            # if active == False:
            check_selection_active(event_id,sport_id)

            return JsonResponse({'message': 'Selection status changed'})
        else:
            return JsonResponse({'error': 'Selection not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def check_selection_active(event_id,sport_id):
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
        else:
            cursor.execute(
                "UPDATE event SET active = %s WHERE id = %s",
                [True, event_id]
            )
        
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

def get_selection_by_id(selection_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific selection by ID
        cursor.execute("SELECT * FROM selection WHERE id = %s", [selection_id])
        selection = cursor.fetchone()

    if selection:
        return True
    return False


@csrf_exempt
@require_http_methods(["POST"])
def search_selection(request):
    data = json.loads(request.body)
    name = data['name']
    active = data['active']
    outcome = data['outcome']
    price_from = data['price_from']
    price_to = data['price_to']
    price_condtion = data['price_condtion']

    
    with connection.cursor() as cursor:

        with connection.cursor() as cursor:

            query = "SELECT * FROM selection as s INNER JOIN event e on e.id = s.event_id WHERE  1=1"
            params = []

            if name != '':
                query += " AND s.name REGEXP %s"
                params.append(name)

            if active != '':
                query += " AND s.active = %s"
                params.append(active)
            
            if outcome != '':
                query += " AND s.outcome = %s"
                params.append(outcome)
            if price_from != '':
                if price_condtion == 'gt':
                    query += " AND price > %s "
                    params.append(price_from)
                elif price_condtion == 'lt':
                    query += " AND price < %s "
                    params.append(price_from)
                elif price_condtion == 'eq':
                    query += " AND price = %s "
                    params.append(price_from)
                else:
                    if price_from != '' and price_to != '':    
                        if price_condtion == 'bw':
                            query += " AND price >= %s AND price <= %s"
                            params.append(price_from)
                            params.append(price_to)

            cursor.execute(query, params)

            selections = cursor.fetchall()
            selection_list = []
            for selection in selections:
                selection_data = {
                    'id': selection[0],
                    'name': selection[1],
                    'event_id': selection[5],
                    'price': selection[2],
                    'active': selection[3],
                    'outcome': selection[4],
                    'sport_id': selection[13]
                }
                selection_list.append(selection_data)
    return JsonResponse({'selections': selection_list})
