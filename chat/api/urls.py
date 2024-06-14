from django.urls import path
from .views.room import rooms_view, single_room_view , room_count_view
from .views.message import message_view, single_message_view

urlpatterns = [
    path('rooms/', rooms_view, name="rooms_view"),
    path('rooms/count/', room_count_view, name="room_count_view"),
    path('rooms/<int:id>/', single_room_view, name="single_room_view"),
    path('rooms/<int:id>/message/', message_view, name="message_view"),
    path('rooms/<int:room_id>/message/<int:id>/', single_message_view, name="single_message_view")
]