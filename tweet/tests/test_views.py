from django.test import TestCase
from django.shortcuts import reverse
from tweet.models import Profile,Tweet
from django.contrib.auth.models import User
from tweet.forms import TweetForm,ImageForm,FileForm
from io import BytesIO
#tweet=Tweet.objects.create()

#user=User.objects.create(username='lekan')
class TestPage(TestCase):
		

	def test_tweet_view(self):
		b=reverse('TweetUrl')
		response=self.client.get(b)
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'tweetTemplate/tweet.html')
		self.assertContains(response,'')

	def test_profile_view(self):
		b=reverse('ProfileUrl',args=[1])
		response=self.client.get(b)
		self.assertEqual(response.status_code,302)
		#self.assertTemplateUsed(response,'tweetTemplate/profile.html')

	def test_create_view(self):
		user=User.objects.create(username='lekan')
		tweet_form=TweetForm({'body':'Hello'})
		invalid_form=TweetForm({'body':''})
		b=reverse('CreateUrl')
		self.client.force_login(user)
		res=self.client.get(b,args=[tweet_form])
		response=self.client.post(b)

		self.assertIsInstance(res.context['form'],TweetForm)
		self.assertTrue(tweet_form.is_valid())
		#self.assertTrue(response.request.user)
		self.assertFalse(invalid_form.is_valid())
		self.assertEqual(response.status_code,302)
		self.assertEqual(res.status_code,200)
		#self.assertTemplateUsed(response,'tweetTemplate/tweet.html')

	# def test_detail_tweet_view(self):
	# 	b=reverse('TweetDetailUrl',args=[1])
	# 	response=self.client.get(b)
	# 	self.assertEqual(response.status_code,200)
	# 	self.assertTemplateUsed(response,'tweetTemplate/tweetDetail.html')

	def test_create_reply_view(self):
		user=User.objects.create(username='lekan')
		b=reverse('ACreateUrl',args=[1])
		self.client.force_login(user)
		response=self.client.get(b)
		self.assertEqual(response.status_code,200)
		#self.assertTemplateUsed(response,'tweetTemplate/profile.html')


	def test_follow_view(self):
		user=User.objects.create(username='lekan')
		b=reverse('FollowUrl',args=[1])
		self.client.force_login(user)
		response=self.client.get(b)
		self.assertEqual(response.status_code,200)
