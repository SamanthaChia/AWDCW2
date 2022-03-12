from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path('register/', user_register_view, name="register"),
    path('login/', user_login_view, name="login"),
    path('logout/', user_logout_view, name="logout"),
    path('search/', user_search_view, name="search"),
    path('<user_id>/', user_view, name="user_view"),
    path('<user_id>/edit/', edit_particulars_view, name="edit"),
    path('<user_id>/edit/cropImg', crop_image_view, name="crop_image"),
]