from django.core.cache import cache
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Location
from .serializers import LocationSerializer
from django.db.models import Avg
import pandas as pd
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
import math
from .renderers import CSVRenderer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().select_related('category', 'created_by')
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['avg_rating', 'created_at']

    def list(self, request, *args, **kwargs):
        cache_key = f"locations_list:{request.get_full_path()}"
        data = cache.get(cache_key)
        if data is not None:
            return Response(data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*5)
        return response

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        cache.clear()

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()

    def get_queryset(self):
        queryset = super().get_queryset().annotate(avg_rating=Avg('reviews__rating'))
        min_rating = self.request.query_params.get('min_rating')
        max_rating = self.request.query_params.get('max_rating')
        if min_rating is not None:
            queryset = queryset.filter(avg_rating__gte=float(min_rating))
        if max_rating is not None:
            queryset = queryset.filter(avg_rating__lte=float(max_rating))
        return queryset

    @action(detail=False, methods=['get'], url_path='export')
    def export(self, request):
        queryset = self.get_queryset()
        data = []
        for loc in queryset:
            avg_rating = getattr(loc, 'avg_rating', loc.rating)
            if avg_rating is not None and (isinstance(avg_rating, float) and math.isnan(avg_rating)):
                avg_rating = None
            data.append({
                'id': loc.id,
                'name': loc.name,
                'description': loc.description,
                'category': str(loc.category),
                'created_by': str(loc.created_by),
                'created_at': loc.created_at,
                'updated_at': loc.updated_at,
                'avg_rating': avg_rating,
            })
        return Response(data) 