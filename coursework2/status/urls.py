from django.urls import path
from . import views

app_name = "status"

urlpatterns = [
    path('', views.timeline, name="timeline"),
    path('<user_id>/', views.status_profile, name="status-profile"),
]