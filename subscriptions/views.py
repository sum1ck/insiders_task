from rest_framework import viewsets, permissions
from .models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.response import Response
from rest_framework import status

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'PATCH not allowed for subscriptions.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    