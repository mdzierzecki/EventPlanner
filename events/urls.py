from django.conf.urls import url
from django.urls import path

from .views import EventAddView, EventListView, EventDeleteView,  EventDetailParticipantAddView, EventUpdateView, \
    ParticipantsListView, ParticipantDeleteView

urlpatterns = [
    path('add-event/', EventAddView.as_view(), name="event_add_view"),
    path('your-events/', EventListView.as_view(), name="user_events_list"),
    path('your-events/<int:id>/delete', EventDeleteView.as_view(), name="event_delete_view"),

    path('your-events/<int:id>/edit', EventUpdateView.as_view(), name="event_update_view"),

    path('your-events/<int:id>/members', ParticipantsListView.as_view(), name="event_members_view"),

    path('your-events/member/<int:id>/delete', ParticipantDeleteView.as_view(), name="member_delete_view"),

    # both for event detail and participant form
    path('info/<int:pk>', EventDetailParticipantAddView.as_view(), name='event_detail'),


]