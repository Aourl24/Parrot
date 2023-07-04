# from rest_framework import serializers
# from .models import Tweet

# class TweetSerializer(serializers.ModelSerializer):
#     profile=serializers.CharField(source='profile.user.username')
#     class Meta:
#         model=Tweet
#         fields=['body', 'date', 'like', 'comment', 'profile']
#         