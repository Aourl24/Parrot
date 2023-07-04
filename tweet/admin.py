from django.contrib import admin
from .models import Tweet, File, Profile, Image, Saves
from django.contrib.auth.models import User

#admin.site.unregister(User)
admin.site.register([Tweet, File,Image, Saves])
admin.site.register(Profile)
