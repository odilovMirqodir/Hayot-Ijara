from django.urls import path
from .views import *

urlpatterns = [
    path('workers/', WorkerListCreateAPIView.as_view(), name='worker-list'),
    path('workers/<int:telegram_id>/', WorkerRetrieveUpdateDestroyAPIView.as_view(), name='worker-detail'),
    path('checkins/', CheckInListCreateAPIView.as_view(), name='checkin-list'),
    path('checkins/<int:telegram_id>/', CheckInRetrieveUpdateDestroyAPIView.as_view(), name='checkin-detail'),
]
