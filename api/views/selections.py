import json

from datetime import datetime

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# CRUD - SELECTION

@csrf_exempt
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

def get_all_selections(request):
    try:
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def get_selection(request, selection_id):
    try:
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)
@csrf_exempt
def update_selection(request, selection_id):
    try:
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
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def delete_selection(request, selection_id):
    try:
        if get_selection_by_id(selection_id):
            with connection.cursor() as cursor:
                # Execute raw SQL query to delete a specific selection by ID
                cursor.execute("DELETE FROM selection WHERE id = %s", [selection_id])

            return JsonResponse({'message': 'Selection deleted'})
        else:
            return JsonResponse({'error': 'Selection not found'}, status=404)
    except Exception as e:
        # Handle other unexpected exceptions
        return JsonResponse({'error': 'An error occurred '+ str(e)}, status=500)

def get_selection_by_id(selection_id):
    with connection.cursor() as cursor:
        # Execute raw SQL query to fetch a specific selection by ID
        cursor.execute("SELECT * FROM selection WHERE id = %s", [selection_id])
        selection = cursor.fetchone()

    if selection:
        return True
    return False
