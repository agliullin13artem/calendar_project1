from django.urls import path
from .views import AddEventView, RemoveEventView, RemoveNextEventsView, UpdateEventView, EventsByDateView




urlpatterns = [
    path('add/', AddEventView.as_view(), name='add_event'),
    path('remove/<int:id>/<int:year>/<int:month>/<int:day>/', RemoveEventView.as_view(), name='remove_event'),
    path('remove-next/<int:id>/<int:year>/<int:month>/<int:day>/', RemoveNextEventsView.as_view(), name='remove_next_event'),
    path('update/<int:id>/<int:year>/<int:month>/<int:day>/', UpdateEventView.as_view(), name='update_event'),
    path('event/<int:year>/<int:month>/<int:day>/', EventsByDateView.as_view(), name='event_date'),
]
