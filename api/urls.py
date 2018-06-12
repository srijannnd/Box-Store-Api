# api/urls.py
from django.urls import path
from api import views

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('staff_user_boxes', views.staff_user_boxes, name="staff_user_boxes"),
    path('list_all_boxes', views.list_all_boxes, name="list_all_boxes"),
]