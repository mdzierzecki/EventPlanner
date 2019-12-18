from django.conf.urls import url
from django.urls import path

from .views import EventAddView, EventListView, EventDeleteView, ParticipantAddView, EventDetailView

urlpatterns = [
    path('add-event/', EventAddView.as_view(), name="event_add_view"),
    path('your-events/', EventListView.as_view(), name="user_events_list"),
    path('your-events/<int:id>/delete', EventDeleteView.as_view(), name="event_delete_view"),
    path('info/<slug:pk>', EventDetailView.as_view(), name='event-detail'),

    # Participants

    path('join/<int:pk>', ParticipantAddView.as_view(), name="participant_add_view"),

]