from django.urls import path
from .views import userView,userReg

urlpatterns=[
	path('home/',userView,name='userUrl'),
	path('createuser/',userReg,name='userReg')
]