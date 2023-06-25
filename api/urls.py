from django.urls import path
from api.views import sports,events,selections,filters

urlpatterns = [
    path('sports/', sports.get_all_sports, name='get_all_sports'),
    path('sports/<int:sport_id>/', sports.get_sport, name='get_sport'),
    path('sports/create/', sports.create_sport, name='create_sport'),
    path('sports/update/<int:sport_id>/', sports.update_sport, name='update_sport'),
    path('sports/delete/<int:sport_id>/', sports.delete_sport, name='delete_sport'),
    
    path('events/create/', events.create_event, name='create_event'),
    path('events/', events.get_all_events, name='get_all_events'),
    path('events/<int:event_id>/', events.get_event, name='get_event'),
    path('events/update/<int:event_id>/', events.update_event, name='update_event'),
    path('events/delete/<int:event_id>/', events.delete_event, name='delete_event'),
    
    path('selections/create/', selections.create_selection, name='create_selection'),
    path('selections/', selections.get_all_selections, name='get_all_selections'),
    path('selections/<int:selection_id>/', selections.get_selection, name='get_selection'),
    path('selections/update/<int:selection_id>/', selections.update_selection, name='update_selection'),
    path('selections/delete/<int:selection_id>/', selections.delete_selection, name='delete_selection'),

    path('sports/regex/<str:regex>/', filters.sports_with_name_regex, name='sports_with_name_regex'),
    path('events/active_threshold/<int:threshold>/', filters.events_with_active_threshold, name='events_with_active_threshold'),
    path('events/timeframe/', filters.events_in_timeframe, name='events_in_timeframe'),
    
]