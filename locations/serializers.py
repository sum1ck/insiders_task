from rest_framework import serializers
from .models import Location
from categories.models import Category

class LocationSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'name', 'description', 'category', 'created_by', 'created_at', 'updated_at', 'rating']
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'rating']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value 