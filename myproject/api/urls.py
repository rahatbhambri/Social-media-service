from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.attemptLogin),
    path('login', views.attemptLogin),
    path('signup', views.signup),
    
    
]
