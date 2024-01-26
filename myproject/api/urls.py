from django.urls import path 
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('', views.homepage),
    path('login', views.attemptLogin),
    path('signup', views.signup),
    path('editFriend', views.reactToFriend),
    path('friends', views.getFriends),
    path('pendingFriends', views.getPendingFriends), 
    path('search', views.searchUsers),
    path('sendMessage', views.sendMessage),
]
