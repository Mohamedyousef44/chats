from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Room {self.id}"


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'id')

    def __str__(self):
        return f"Message {self.id} in Chat Room {self.room.id}"


class AppMeta(models.Model):
    meta_key  = models.CharField(max_length=50)
    meta_value = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)