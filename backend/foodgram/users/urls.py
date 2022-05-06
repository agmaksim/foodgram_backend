from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CustomUserViewSet

router_v1 = SimpleRouter()

router_v1.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('api/', include(router_v1.urls)),
    path('api/auth/', include('djoser.urls.authtoken'))
]
