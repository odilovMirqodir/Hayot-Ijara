from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('worker/<int:worker_id>/', views.worker_detail, name='worker_detail'),
    path('test-404/', views.test_404),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
