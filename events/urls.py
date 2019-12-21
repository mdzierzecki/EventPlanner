from django.conf.urls import url
from django.urls import path

from .views import EventAddView, EventListView, EventDeleteView,  EventDetailView

urlpatterns = [
    path('add-event/', EventAddView.as_view(), name="event_add_view"),
    path('your-events/', EventListView.as_view(), name="user_events_list"),
    path('your-events/<int:id>/delete', EventDeleteView.as_view(), name="event_delete_view"),

    # both for event detail and participant form
    path('info/<int:pk>', EventDetailView.as_view(), name='event-detail'),


]