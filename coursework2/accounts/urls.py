from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('register/', user_register, name="register"),
    path('login/', user_login, name="login"),
    path('<user_id>/', user_view, name="user_view"),
    path('<user_id>/edit/', edit_particulars, name="edit"),
    path('<user_id>/edit/cropImg', crop_image, name="crop_image"),
]