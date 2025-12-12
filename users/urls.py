from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserRegistrationViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'register', UserRegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]
