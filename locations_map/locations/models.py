from django.db import models
from django.conf import settings

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE, related_name='locations')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='locations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([r.rating for r in reviews]) / reviews.count(), 2)
        return None 