from django.shortcuts import render,redirect
from .forms import Register

# Create your views here.
def userView(request):
	b=request.META['REMOTE_ADDR']
	#d=request.META['HTTP_X_FORWARDED_FOR']
	print('ip address' ,b)
	template='userTemplate/index.html'
	context=dict(content='')

	return render (request, template)


def userReg(request):
	form=Register()
	template='userTemplate/register.html'
	
	if request.method=='POST':
		form=Register(request.POST)
		b=request.META('REMOTE_ADDR')
		if form.is_valid():
			form.save()

			return redirect('userUrl')

	context=dict(form=form)

	return render(request,template,context)