from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'registrations', RegistrationViewSet, basename='registration')
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]
