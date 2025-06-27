from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Review
from .serializers import ReviewSerializer
from django.core.mail import send_mail
from subscriptions.models import Subscription
from django.core.cache import cache

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('location', 'user')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location', 'user', 'rating']
    search_fields = ['text']
    ordering_fields = ['created_at', 'rating']

    def list(self, request, *args, **kwargs):
        cache_key = f"reviews_list:{request.get_full_path()}"
        data = cache.get(cache_key)
        if data is not None:
            return Response(data)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*5)
        return response

    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)
        location = review.location
        subscriptions = Subscription.objects.filter(location=location).select_related('user')
        emails = [sub.user.email for sub in subscriptions if sub.user.email]
        if emails:
            send_mail(
                subject=f'New review for {location.name}',
                message=f'User {review.user.username} left a new review: "{review.text}" (rating: {review.rating})',
                from_email=None,
                recipient_list=emails,
                fail_silently=True,
            )
        cache.clear()

    def perform_update(self, serializer):
        serializer.save()
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()

    def get_queryset(self):
        queryset = super().get_queryset()
        location_id = self.request.query_params.get('location')
        if location_id:
            queryset = queryset.filter(location_id=location_id)
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        review = self.get_object()
        review.likes.add(request.user)
        review.dislikes.remove(request.user)
        return Response({'status': 'liked'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        review = self.get_object()
        review.dislikes.add(request.user)
        review.likes.remove(request.user)
        return Response({'status': 'disliked'}) 