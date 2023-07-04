from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals  import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import reverse, redirect
from .cell import Cell
from twitter.settings import BASE_DIR
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    user=models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    follower=models.ManyToManyField('self', related_name='follow', symmetrical=False, blank=True)
    date_joined=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    bio=models.CharField(max_length=100, blank=True, null=True)
    location=models.CharField(max_length=100, blank=True, null=True)
    profile_photo=models.ImageField(upload_to='profileimage', default='profileimage/profile.png', null=True, blank=True)
    cover_photo=models.ImageField(upload_to='profileimage', null=True, blank=True)
    mode=models.CharField(max_length=100, default='white')
    
    def __str__(self):
        return self.user.username
        
    def get_absolute_url(self):
        return reverse('ProfileUrl', args=[self.id])


class Tweet(models.Model):
    profile=models.ForeignKey(Profile,related_name='tweet', on_delete=models.CASCADE, blank=True)
    date=models.DateTimeField(auto_now_add=True)
    body=models.TextField()
    like=models.ManyToManyField(Profile,related_name='liked', blank=True)
    comment=models.ForeignKey('self', related_name='tweet', null=True, blank=True, on_delete=models.CASCADE)
    views=models.ManyToManyField(Profile,related_name='viewed', blank=True)
    active=models.BooleanField(default=True)
    retweet=models.ManyToManyField(Profile,related_name='retweet', blank=True)



    def get_absolute_url(self):
        return reverse ('TweetDetailUrl', args=[self.id])

    def most_word(self):
        #h=Cell(self.body)
        #jh=h.most('word')
        #self.body=self.body.replace(',"',' ')
        self.body=self.body.split(' ')
        self.bod=[i for i in self.body if len(i) >= 4]
        #print(self.body)
        d=sorted(self.bod,key=lambda i: self.bod.count(i), reverse=True)

        return d
        
    def Delete(self):
        self.delete()
        #return redirect('TweetUrl')
        
    def __str__(self):
        return self.body    
    

class Image(models.Model):
    tweet=models.ForeignKey(Tweet, related_name='image', on_delete=models.CASCADE, null=True, blank=True)
    image=models.ImageField(upload_to='images', blank=True)   
    
    def __str__(self):
        return 'Image '  + str(self.id)
        
    def get_absolute_url(self):
        return reverse('ImageUrl', args=[self.id])
        
class File(models.Model):
    tweet=models.ForeignKey(Tweet, related_name='file', on_delete=models.CASCADE, blank=True, null=True)
    file=models.FileField(upload_to='files', blank=True) # validators=[FileExtensionValidator(allowed_extensions=['.mp4',''])]

    def __str__(self):
        return 'File '  + str(self.id)

class Saves(models.Model):
    profile=models.OneToOneField(Profile, related_name='saves', on_delete=models.CASCADE)
    tweets=models.ManyToManyField(Tweet, related_name='saved', blank=True,) 

    def __str__(self):
        return self.profile.user.username  + 'Saves'
        
        
@receiver(post_save, sender=User)    
def created_profile(sender, instance, created,  **kwargs):
    if created:
        user_profile=Profile(user=instance)
        user_profile.save()
        user_profile.follower.set([instance.profile.id])
        user_profile.profile_photo='media/profile.png'
                     