from django.db import models
from django.conf import settings

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    location = models.ForeignKey('locations.Location', on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        unique_together = ('user', 'location')

    def __str__(self):
        return f'{self.user.username} subscribed to {self.location.name}' 