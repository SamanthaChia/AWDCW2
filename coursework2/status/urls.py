from django.urls import path
from .views import *

app_name = "status"

urlpatterns = [
    path('', timeline_view, name="timeline"),
    path('<user_id>/', status_profile_view, name="status-profile"),
]