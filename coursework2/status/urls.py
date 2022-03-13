from django.urls import path
from .views import *

app_name = "status"

urlpatterns = [
    path('', timeline, name="timeline"),
    path('<user_id>/', status_profile, name="status-profile"),
]