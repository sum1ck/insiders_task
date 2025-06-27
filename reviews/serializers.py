from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    dislikes_count = serializers.IntegerField(source='dislikes.count', read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'location', 'user', 'text', 'rating', 'likes_count', 'dislikes_count', 'created_at']
        read_only_fields = ['user', 'likes_count', 'dislikes_count', 'created_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value 