from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('<user_id>/', views.user_view, name="user_view"),
    path('<user_id>/edit/', views.edit_particulars, name="edit"),
    path('<user_id>/edit/cropImg', views.crop_image, name="crop_image"),
]