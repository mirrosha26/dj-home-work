from django.urls import path
from .views import SensorView, SensorDetailView, CreateSensorView

urlpatterns = [
    path('sensors/', SensorView.as_view()),
    path('sensors/<int:pk>/', SensorDetailView.as_view()),
    path('measurements/', CreateSensorView.as_view()),
]
