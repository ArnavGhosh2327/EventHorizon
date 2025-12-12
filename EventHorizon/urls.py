from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from rest_framework.authtoken.views import obtain_auth_token

import os


admin.site.site_header = os.getenv("DJANGO_SITE_HEADER", "Event Horizon")
admin.site.site_title = os.getenv("DJANGO_SITE_TITLE", "Event Horizon")
admin.site.index_title = os.getenv("DJANGO_INDEX_TITLE", "Event Horizon")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include(oauth2_urls)),
    path('accounts/', include('allauth.urls')),
    
    # API endpoints
    path('api/', include('events.urls')),
    path('api/users/', include('users.urls')),
    path('api/', include('registrations.urls')),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
]
