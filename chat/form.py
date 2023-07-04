from django import forms
from .models import Messages

class MyForm(forms.ModelForm):
	class Meta:
		model=Messages
		fields=['body']
