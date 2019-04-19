from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()  # Default user <--- Change this later?

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username

    def last_10_messages():
        result = list(Message.objects.order_by('-timestamp').all())  # Return the ALL historical messages
        result.reverse()
        return result