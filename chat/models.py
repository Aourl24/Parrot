from django.db import models
from django.contrib.auth.models import User
from tweet.views import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth import user_logged_in,user_logged_out


class Chat(models.Model):
	user=models.OneToOneField(User,related_name='chat',on_delete=models.CASCADE)
	active=models.BooleanField(default=True)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self): 
		return reverse('message',args=[self.id])

	def disactivate(self):
		Chat.objects.get(id=id).active=False

class GroupChat(models.Model):
	name=models.CharField(max_length=1000)
	member=models.ManyToManyField(User,blank=True,related_name='group',symmetrical=False)
	active=models.BooleanField(default=True)

class Messages(models.Model):
	receiver=models.ForeignKey(Chat,related_name='receiver_messages',on_delete=models.CASCADE,null=True,blank=True)
	group=models.ForeignKey(GroupChat,related_name='messages',on_delete=models.CASCADE,null=True,blank=True)
	sender=models.ForeignKey(Chat,related_name='sender_messages',on_delete=models.CASCADE,blank=True,null=True)
	body=models.TextField()
	time=models.DateTimeField(auto_now_add=True)
	reply=models.ManyToManyField('self',symmetrical=False,related_name='replys',blank=True)


	def __str__(self):

		return self.body[:10]

@receiver(post_save,sender=User)
def ChatSignal(sender,instance,created,**kwargs):
	if created:
		Chat.objects.create(user=instance,active=True)
		

@receiver(post_save,sender=user_logged_out)
def LogSignal(sender,instance,created,**kwargs):
	if created:
		d=Chat.objects.get(user=instance)
		d.active=False
		d.save()