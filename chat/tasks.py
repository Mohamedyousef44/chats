from celery import shared_task
from chat.models import Room, AppMeta

@shared_task
def update_room_count():
    room_count = Room.objects.count()
    AppMeta.objects.update_or_create(
        meta_key='rooms_count',
        defaults={'meta_value': str(room_count)}
    )
