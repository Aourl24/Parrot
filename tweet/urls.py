from django.urls import path, include
from .views import TweetView, CreateTweet, ImageView, \
ProfileView, FollowView, EditProfileView, TweetDetailView, NotificationView,  \
CommentView, TrendingView, TrendingRedirect, ModeView, FriendView, SearchView, \
FollandFollowerView, HomeView , OptionView, SaveView, DeleteView , landingView

# from rest_framework import routers TweetApi

# route=routers.DefaultRouter()
# route.register(f'tweet', TweetApi)

urlpatterns=[
    path('',landingView,name="LandingUrl"),
    path('tweets/',TweetView, name='TweetUrl' ),
    path('create/', CreateTweet, name='CreateUrl'), 
    path('<int:id>/create/', CreateTweet, name='ACreateUrl'),
    path('<int:id>/img', ImageView, name='ImageUrl'), 
    path('<int:id>/prof', ProfileView, name='ProfileUrl'), 
    path('<int:id>/follow',FollowView, name='FollowUrl'), 
    path('edit/', EditProfileView, name='EditProfUrl'),
    path('<int:id>detail', TweetDetailView, name='TweetDetailUrl'),
    path('notify/', NotificationView, name='NotificationUrl'),
    path('comment/', CommentView, name='CommentUrl'),
    path('trending/', TrendingView, name='TrendUrl'),
    path('<str:word>trendingRedirect/', TrendingRedirect, name='TrendRed'), 
    path('mode/', ModeView, name='ModeUrl'),
    path('friend/',FriendView,name='FriendUrl'),
    path('search/',SearchView,name='SearchUrl'),
    path('<int:id>followdet',FollandFollowerView,name='FollowListUrl'),
    path('<int:fid>follow',FollandFollowerView,name='FollowerListUrl'),
    path('home/', HomeView, name='HomeUrl'), 
    path('latest<str:lat>/', TweetView, name='LatestTweetUrl'),
    path('home<str:hom>/', TweetView, name='HomeTweetUrl'), 
    path('option/', OptionView, name='OptionUrl'), 
    path('save/', SaveView, name='SaveUrl'), 
    path('delete/<int:id>', DeleteView, name='DeleteUrl')
]
    #path('followdet',FollandFollowerView,name='FollowListUrl'),
    #path('follow',FollandFollowerView,name='FollowerListUrl')

    #path('', include(route.urls))
