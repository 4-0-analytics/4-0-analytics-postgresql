from django.urls import path, re_path
from emcar import views

urlpatterns = [
    re_path(r'^api/emcar$', views.group_list),
    re_path(r'^api/emcar/(?P<pk>[0-9]+)$', views.group_detail),
    re_path(r'^api/emcar/published$', views.group_list_published),
    path('vehicles/',
         views.vehicle_list,
         name='vehicle-list'),
    path('vehicles/<int:pk>/',
         views.vehicle_detail,
         name='vehicle-detail'),
    path('task/',
         views.client_list,
         name='client-list'),
    path('task/<int:pk>/',
         views.client_detail,
         name='client-detail'),
    path("users/", views.UserList.as_view(), name="user-list"),  # new
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),  # new
    path("getVehicles/", views.get_Vehicles, name="index"),
    path('basic', views.YourView.as_view()),
    path("register", views.register, name="register"),
    path("login_user", views.login_user, name="login_user"),
    path("logout_user", views.logout_user, name="logout_user"),
    path("home", views.home, name="home"),
    path("", views.api_root),
]
