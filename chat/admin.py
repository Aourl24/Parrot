from django.contrib import admin
from .models import Messages,Chat,GroupChat

admin.site.register([Messages,Chat,GroupChat])
