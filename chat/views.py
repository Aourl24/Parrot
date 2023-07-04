from django.shortcuts import render,redirect
from .form import MyForm
from .models import Messages,Chat,GroupChat
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from notifications import notify
from tweet.models import Profile

@login_required
def ChatView(request):
    prof=Profile.objects.get(user__username=request.user)
    fo=prof.follow.all()
    fol=prof.follower.all()
    foll=User.objects.filter(profile__in=fo)
    profile=User.objects.all()
    follo=User.objects.filter(profile__in=fol)
    chat=Chat.objects.all().exclude(user=request.user).filter(user__in=foll).filter(user__in=follo)
    template='messageTemplate/chat.html'
    context=dict(chat=chat) 
    return render(request,template,context)


@login_required
def MessageView(request,id):
	cha=Chat.objects.get(id=id)
	send=Chat.objects.get(user__username=request.user)

	form=MyForm()
	if request.method=='POST':
		form=MyForm(request.POST)

		if form.is_valid():
			b=form.save(commit=False)
			b.sender=Chat.objects.get(user__username=request.user)
			b.receiver=Chat.objects.get(id=id)
			b.save()
			notify.send(request.user, recipient=User.objects.get(chat=cha), verb='New message ', description=cha.get_absolute_url())
			return redirect(request.path_info)

	first=Messages.objects.filter(sender=send,receiver=cha)
	second=Messages.objects.filter(sender=cha,receiver=send)
	chat=first.union(second)
	user=User.objects.get(username=request.user)

	template='messageTemplate/index.html'

	context=dict(form=form,chat=chat,cha=cha,User=send)
	if 'HX-Request' in request.headers:
		template='messageTemplate/message.html'
		return render(request,template,context)


	context=dict(form=form,chat=chat,cha=cha,User=send)
	return render (request,template,context)