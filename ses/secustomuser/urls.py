
from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views 
urlpatterns = [
    #url for home page
    path('', views.Home,name='home'),

    #url for a create role
    path('role/',views.create_role,name='role'),
    #url for login at SEM
    path('login/',views.Login,name='loginPage'),
    #url for Register SEM
    path('register/',views.Register,name='register'),
    #url for getting user details
    path('getuser/',views.getuser,name='getuser'),
    #url for getting created apps
    path('getapp/',views.getapp,name='getapp'),

    # path('loginPage/', views.LoginPage,name='loginPage'),
    # path('login/', auth_views.LoginView.as_view(template_name='auth/Login.html'), name='login'),
 

]