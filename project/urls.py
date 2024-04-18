
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('register/', views.UserRegistration.as_view(), name='user_register'),
    path("login/", views.UserSignIn.as_view(), name="user_login"),
    path("home/<str:username>/", views.Home.as_view(), name="home"),
    path('logout/', views.UserLogout.as_view(), name='user_logout'),
    path('home/', views.Home.as_view()),
]
