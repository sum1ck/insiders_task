from rest_framework.routers import DefaultRouter
from locations.views import LocationViewSet
from categories.views import CategoryViewSet
from reviews.views import ReviewViewSet
from subscriptions.views import SubscriptionViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription') 