from django.urls import path
from .views import MessageView,ChatView


urlpatterns=[
	path('<int:id>msg/',MessageView,name='message'),
	path('chat/',ChatView,name='chat')
]