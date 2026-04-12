from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.api.urls')),
    path('api/cases/', include('cases.api.urls')),
    path('api/users/', include('users.api.urls')),
    path('api/trades/', include('trades.api.urls')),
    path('api/gangs/', include('gangs.api.urls')),
]
