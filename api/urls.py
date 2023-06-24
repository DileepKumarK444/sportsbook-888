from django.urls import path
from api import views

urlpatterns = [
    path('sports/', views.get_all_sports, name='get_all_sports'),
    path('sports/<int:sport_id>/', views.get_sport, name='get_sport'),
    path('sports/create/', views.create_sport, name='create_sport'),
    path('sports/update/<int:sport_id>/', views.update_sport, name='update_sport'),
    path('sports/delete/<int:sport_id>/', views.delete_sport, name='delete_sport'),
    
    path('events/create/', views.create_event, name='create_event'),
    path('events/', views.get_all_events, name='get_all_events'),
    path('events/<int:event_id>/', views.get_event, name='get_event'),
    path('events/<int:event_id>/update/', views.update_event, name='update_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    
    path('selections/create/', views.create_selection, name='create_selection'),
    path('selections/', views.get_all_selections, name='get_all_selections'),
    path('selections/<int:selection_id>/', views.get_selection, name='get_selection'),
    path('selections/<int:selection_id>/update/', views.update_selection, name='update_selection'),
    path('selections/<int:selection_id>/delete/', views.delete_selection, name='delete_selection'),

    path('sports/regex/<str:regex>/', views.sports_with_name_regex, name='sports_with_name_regex'),
    path('events/active_threshold/<int:threshold>/', views.events_with_active_threshold, name='events_with_active_threshold'),
    path('events/timeframe/', views.events_in_timeframe, name='events_in_timeframe'),
    
]