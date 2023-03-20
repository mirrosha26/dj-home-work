from django.urls import path
from .views import *

urlpatterns = [
    path('<str:key>/', calculator_views, name='calculator'),
]