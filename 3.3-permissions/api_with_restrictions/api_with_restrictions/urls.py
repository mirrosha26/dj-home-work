from django.contrib import admin
from django.urls import path, include
from advertisements.views import AdvertisementViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('advertisements', AdvertisementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
