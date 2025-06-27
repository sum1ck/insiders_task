import audioop
from rest_framework import viewsets, permissions
from .models import Category
from .serializers import CategorySerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated] 

    def list(self, request, *args, **kwargs):
        cache_key = f"categories_list:{request.get_full_path()}"
        data = cache.get(cache_key)
        if data is not None:
            return Response(data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*5)
        return response

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'PATCH not allowed for categories.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        serializer.save()
        cache.clear()

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()