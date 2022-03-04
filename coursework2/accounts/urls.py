from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('<user_id>/', views.user_view, name="user_view")
]