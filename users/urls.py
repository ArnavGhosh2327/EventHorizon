from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, UserRegistrationViewSet, MFAViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'register', UserRegistrationViewSet, basename='register')
router.register(r'mfa', MFAViewSet, basename='mfa')

urlpatterns = [
    path('', include(router.urls)),
]
