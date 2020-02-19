from django.conf.urls import url
from django.urls import path

from .views import EventAddView, EventListView, EventDeleteView,  EventDetailParticipantAddView, EventUpdateView, \
    EventPanelView, ParticipantDeleteView, ParticipantSuccessAddView, participant_export_csv, \
    participant_self_delete_view, participant_self_delete_succcess, participant_self_delete_error


urlpatterns = [
    path('add-event/', EventAddView.as_view(), name="event_add_view"),
    path('your-events/', EventListView.as_view(), name="user_events_list"),
    path('your-events/<int:id>/delete', EventDeleteView.as_view(), name="event_delete_view"),

    path('your-events/<int:id>/edit', EventUpdateView.as_view(), name="event_update_view"),

    path('your-events/<int:id>/panel', EventPanelView.as_view(), name="event_panel_view"),

    path('your-events/member/<int:id>/delete', ParticipantDeleteView.as_view(), name="member_delete_view"),

    # member self delete
    path('member/self-delete', participant_self_delete_view, name="member_self_delete_view"),
    path('member/delete/success', participant_self_delete_succcess, name="member_self_delete_success"),
    path('member/delete/error', participant_self_delete_error, name="member_self_delete_error"),

    # both for event detail and participant form
    path('event/<int:pk>', EventDetailParticipantAddView.as_view(), name='event_detail'),

    # success page
    path('event/<int:pk>/thanks', ParticipantSuccessAddView.as_view(), name='participant_successful'),

    # csv export
    path('export/<int:event_pk>', participant_export_csv, name="export_csv"),


]