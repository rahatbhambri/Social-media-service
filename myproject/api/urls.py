from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.attemptLogin),
    path('login', views.attemptLogin),
    path('signup', views.signup),
    path('editFriend', views.reactToFriend),
    path('friends', views.getFriends),
    path('pendingFriends', views.getPendingFriends), 
    
]
