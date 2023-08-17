from django.shortcuts import render, redirect
from .models import Profile, Tweet, File, Image, Saves
from .forms import TweetForm, FileForm, ImageForm, ProfileForm
from django.http import JsonResponse,HttpResponse
from django.core import serializers
#from rest_framework import viewsets
#from .serializer import TweetSerializer
from django.core.exceptions import ObjectDoesNotExist
from notifications.signals import notify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .cell import Cell
from django.db.models import Subquery
from django.core.paginator import Paginator
from random import shuffle


# CreateTweet functions helps to create tweet, image, file also linking them together. 
#It also helps check whether a user is replying or posting a tweets
#It requires a user to login to load this view

def UserProfile(x):
    return Profile.objects.get(user__username=x) # get the users with the profile instance
 

def landingView(request):
    template = "tweetTemplate/landing.html"
    return render(request,template)

@login_required
def CreateTweet(request, id=None):
    template='tweetTemplate/createTweet.html' 
    tweet_form=TweetForm() #Tweet form instance
    image_form=ImageForm() #image form instance
    file_form=FileForm() #file form instance
    
    if request.method=='POST':
        reply=request.POST.get('reply') #get the reply value from ther request, this is to check whether the tweet is a reply tweet or a normal tweet
        tweet_form=TweetForm(request.POST)
        image_form=ImageForm(request.POST, request.FILES)
        file_form=FileForm(request.POST, request.FILES)
        
        if tweet_form.is_valid(): #check if tweet form is valid
            
            a=tweet_form.save(commit=False) #save the tweet_form temporary
            a.profile=Profile.objects.get(user__username=request.user) #link the tweet to the request user i.e current user
            #Note: The profile of the tweet will always be the request user, he is always the one sending the request to the view
            
            if reply: # if reply is not None that means the tweet is reply to another tweet
                a.comment=Tweet.objects.get(id=reply) # then bind the reply tweet to the original tweet 
                  
            b=a.save() # then finally the tweet 
            
            if image_form.is_valid(): #check if image form is valid
                
                imag=request.FILES.getlist('image') #get the list of images from the request
                
                
                for img in imag: # loop through the images
                    Image.objects.create(image=img, tweet=a) # create image for each instance and link it to our tweet(a)
                #print('list', imag)
               
            if file_form.is_valid(): #check if the file form is valid
                g=file_form['file'].value()
                if g != None:
                    k=g.name
                    if k.endswith('.mp4'): # this is not save tho, but i used it to verify the type of file uploaded
                        d=file_form.save(commit=False) # save it temporary 
                        d.tweet=a #link the file  form to the tweet
                        d.save() # save the file form
            

            if reply:
                # the reason for this is that when a user is replying he is definitely on the tweet detail page , so it is best we return the tweet detail page
                return redirect('TweetDetailUrl',id=int(reply))
        return redirect('TweetUrl') # redirect to the tweet page
        
    context=dict(form=tweet_form, image=image_form, file=file_form)          
    return render(request, template, context)
    
def HomeView(request):
    
    return (request, 'tweetTemplate/home.html')
    
    
# the Tweet View display tweets page by page
# it like tweet
# it retweet twweet

def TweetView(request, lat=None, hom=None):
    blak = False # set blank to false to know whether there is tweets available or not
    
    try:
        # i use try so the user can view the page without login in
        prof=Profile.objects.get(user__username=request.user) # get the request.user with the profile instance
        foll=prof.follow.all() #get the number of followers of request.user
        profile=Profile.objects.all() #get all profiles
        
        
    except (ObjectDoesNotExist, AttributeError):
        # if the user is not login it will just show random tweets to the user
        prof=''
        tweetss=Tweet.objects.all().filter(active=True)


    home_color='#1DA1F2'
    latest_color ='white'
    
    if  lat: #request.session['latest'] == True or lat: #check if the user has asked for latest tweets before or he just asked for it
        latest=True
        home_color='white'
        latest_color ='#1DA1F2'
        tweets=Tweet.objects.all().filter(active=True).filter(profile__in=foll)#.order_by('?') #get the tweets which are active and which the request user follows
        retweets=Tweet.objects.all().filter(retweet__in=foll) #get the tweets that was retweet by those the user follow 
        tweetss=tweets.union(retweets)#combine the tweets and retweets together
        request.session['latest'] =True
    
    elif hom:#request.session['latest'] == False or hom:
        latest=False
        tweetss = Tweet.objects.filter(active=True)
        request.session['latest'] = False

    else:
        tweetss=Tweet.objects.filter(active=True)


    if len(list(tweetss)) == 0: # if the tweet list is none, like when the user just sign up
        blank=True
    else:
        blank=False

    if hom: #if the user request for the home page we set latest back to false
        latest=False

        
        home_color='#1DA1F2'
        latest_color ='white'
        
    
        #shuffle(tweetss)# shuffle the tweets so it can display randomly
    
    page=Paginator(tweetss,5) # i page the tweets this save the page from overhead loading, so it send the tweets page by page

    
    page_no=request.GET.get('page') # get the page number from the request
    tweets=page.get_page(page_no) # get the tweets from that page
    
    
    context=dict(tweets=tweets, tweet=tweets, blank=blank, prof=prof, User=prof, latest=latest_color, home=home_color)
    template='tweetTemplate/tweet.html'
    
    if tweets.has_previous(): # if the tweet has previous page then he is not the starting page, so the template should update some part not fully part
        template='tweetTemplate/tweetbox.html'
    
    # the like condition
    if 'HX-Request' in request.headers and 'like' in request.GET: # check whether the user send request to like
        if request.user.is_authenticated:   # if the user is authenticate i.e log in user
            if request.method=='GET':
                a=request.GET.get('like') # get the like tweet id
                
                try:
                    tweetTo=Tweet.objects.get(id=a) # get the tweet to be like
                
                   
                    prof=Profile.objects.get(user__username=request.user) # get the user that like
                    tweet=tweetTo.like.filter(user__username=request.user).exists() # check if the user as liked the tweets before
                    
                    if tweet: # if user has already liked
                        tweetTo.like.remove(prof) # remove the user

                    else: # if user has not liked
                        tweetTo.like.add(prof) # add the user
                        # send notifications to the user that tweets the post that some liked his tweets
                        notify.send(request.user, recipient=User.objects.get(username=tweetTo.profile.user.username), verb=' Liked your tweet', description=tweetTo.get_absolute_url())
                
                except ObjectDoesNotExist:
                    tweetTo=''
                dd=dict(tweet=tweetTo, prof=prof)
                
                return render(request, 'tweetTemplate/like.html', dd)
                
        else:
            return HttpResponse("<button><i class='far fa-heart'></i></button>  ")
    
    # check whether a tweet is retweet
    if 'HX-Request' in request.headers and 'retweet' in request.GET:

        try:
            prof=Profile.objects.get(user__username=request.user)
            tweet_to_retweet_id=request.GET.get('retweet')
            tweet_to_retweet=Tweet.objects.get(id=tweet_to_retweet_id)

            check=tweet_to_retweet.retweet.filter(user__username=request.user).exists()

            if check:
                tweet_to_retweet.retweet.remove(prof)
            else:
                tweet_to_retweet.retweet.add(prof)  
                notify.send(request.user, recipient=User.objects.get(username=tweet_to_retweet.profile.user.username), verb=' Retweet your tweet', description=tweet_to_retweet.get_absolute_url())
        except ObjectDoesNotExist:
            tweet_to_retweet=''

        print(tweet_to_retweet)
        dd=dict(tweet=tweet_to_retweet,prof=prof)

        return render(request,'tweetTemplate/retweet.html',dd)


    return render(request, template, context=context)
            


# class TweetApi(viewsets.ModelViewSet):
#     queryset=Tweet.objects.all().filter(active=True)
#     serializer_class=TweetSerializer   

# the image preview url
def ImageView(request, id):
    Img=Image.objects.get(id=id)
    template='tweetTemplate/image.html'
    context=dict(image=Img)
    return render(request, template, context)
    
    
@login_required
def ProfileView(request, id):
    profile=Profile.objects.get(id=id)
    
    try:
        prof=Profile.objects.get(user__username=request.user)
    except:
        prof=''
    
    user=Profile.objects.get(user=request.user)
    tweets=Tweet.objects.filter(profile=profile)
    template='tweetTemplate/profile.html'
    context=dict(profile=profile, tweets=tweets, User=user, prof=prof)
    
    return render(request, template, context)

@login_required   
def FollowView(request, id):
    prof=Profile.objects.get(id=id)
    user=Profile.objects.get(user=request.user)
    a=prof.follower.filter(user=request.user).exists()
    
    if a:
        prof.follower.remove(user)
    else:
        prof.follower.add(user)
        notify.send(request.user, recipient=User.objects.get(profile=prof), verb=' Followed You')
    
    template='tweetTemplate/follow.html'
    context=dict(profile=prof, User=user)
    
    return render(request, template, context)
    
@login_required
def EditProfileView(request):
    profile=Profile.objects.get(user=request.user)
    form=ProfileForm(instance=profile)
    
    if request.method=='POST':
        form=ProfileForm(request.POST, request.FILES,  instance=profile)
        if form.is_valid():
            form.save()
            
        return redirect('ProfileUrl', profile.id)
    
    template='tweetTemplate/editProfile.html'
    context=dict(form=form)
    
    return render(request, template, context)
    
   
def TweetDetailView(request, id):
    tweet=Tweet.objects.get(id=id)
    tweet_form=TweetForm()
    image_form=ImageForm()
    file_form=FileForm()

    try:
        prof=Profile.objects.get(user__username=request.user)
    except:
        prof=''
    
    template='tweetTemplate/tweetDetail.html'
    context=dict(tweet=tweet, prof=prof,form=tweet_form,image=image_form,file=file_form)
    
    return render(request, template, context)

@login_required  
def NotificationView(request):
    notifications=request.user.notifications.unread()
    notifications.mark_all_as_read()
    
    return render(request, 'tweetTemplate/notify.html')
    
def CommentView(request):
    
    if request.method=='POST':
        a=request.POST.get('detail')
        b=request.POST.get('body')
        user=Profile.objects.get(user=request.user)
        tweet=Tweet.objects.get(id=int(a))
        Tweet.objects.create(profile=user,body=b,comment=tweet )

        return redirect('TweetDetailUrl', tweet.id)
        
def TrendingView(request):
    Most=[]
    template = 'tweetTemplate/trending.html'
    tweets=Tweet.objects.all()
    
    for tweet in tweets:
        Most=Most + tweet.most_word()
    
    print(Most)
    Top=sorted(Most,key=lambda i: Most.count(i), reverse=True)
    Top.sort()
    Top=set(Top)
    if 'HX-Request' in request.headers:
        template = 'tweetTemplate/trendbox.html'

    context=dict(trends=list(Top)[:10])
    return render(request, template , context)
        
def TrendingRedirect(request, word):
    tweets=Tweet.objects.filter(body__icontains=word)
    try:
        prof=Profile.objects.get(user__username=request.user)
    except:
        prof=''
        
    if 'HX-Request' in request.headers:
        return JsonResponse(int(f'{tweets.count() + sum([x.retweet.count() for x in tweets])}'), safe=False)

    context=dict(tweets=tweets, prof=prof, word=word)
    return render(request, 'tweetTemplate/trendRed.html', context)

@login_required   
def ModeView(request):
    prof=Profile.objects.get(user__username=request.user)
    b=request.GET.get('dark')
    if prof.mode == 'white':
        prof.mode = 'black'
        prof.save()
    else:
        prof.mode = 'white'
        prof.save()
    return redirect(b)


def FriendView(request):
    prof=User.objects.get(username=request.user).profile.follow.all()
    user=Profile.objects.get(user=request.user)
    profile=Profile.objects.all()
    addfriend=User.objects.all().exclude(profile__in=prof)
    template='tweetTemplate/friend.html'
    context=dict(people=addfriend,User=user)
    return render(request,template,context)


def SearchView(request):

    if 'search' in request.GET:
        word=request.GET.get('search')
        checkTweets=Tweet.objects.filter(body__icontains=word)
        checkProfile=Profile.objects.filter(user__username__icontains=word)
    
    user=User.objects.get(username=request.user)
    template='tweetTemplate/search.html'
    context=dict(tweets=checkTweets,people=checkProfile,User=user)
    return render (request,template,context)
    
def FollandFollowerView(request,id=None,fid=None):
    if id:
        profile=Profile.objects.get(id=id)
        profile_foll=profile.follow.all()
        fo='done'
        
    if fid:
        profile=Profile.objects.get(id=fid)
        profile_foll=profile.follower.all()
        fo=None
    #else:
#        profile=Profile.objects.get(user=request.user)
#        profile_foll=profile.
    
    context=dict(profiles=profile_foll, fo=fo, profile=profile)
    template='tweetTemplate/followlist.html'    
    
    return render(request,template,context)
    
  
def OptionView(request):
    save_id= request.GET.get('like')
    prof=UserProfile(request.user)
    tweet=Tweet.objects.get(id=save_id)
    print(save_id)
    
    if save_id:
        pass
    
    context=dict(saveId=save_id, tweet=tweet, prof=prof)
    return render(request, 'tweetTemplate/option.html', context)
    
def SaveView(request):
    Saved=Saves.objects.get(profile=UserProfile(request.user)).tweets.all()
    
    if request.method == 'POST':
        save_id= request.POST.get('save')
        print(save_id)
        tweet=Tweet.objects.get(id=save_id)
        
        try:
            user_save=Saves.objects.get(profile=UserProfile(request.user))
            user_save.tweets.add(tweet)
            user_save.save()
                     
        except ObjectDoesNotExist:
            saving=Saves.objects.create(profile=UserProfile(request.user))
            saving.tweets.add(tweet)
            saving.save()
            
        return HttpResponse('Tweet is Saved')
    
    template='tweetTemplate/save.html'
    context = dict(tweets=Saved) 
      
    return render(request,template, context)
    
def DeleteView(request, id):
    tweet=Tweet.objects.get(id=id)
    tweet.Delete()
    
    return redirect('TweetUrl')
    
    