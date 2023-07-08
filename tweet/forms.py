from django import forms
from .models import Tweet, File,  Image, Profile

class TweetForm(forms.ModelForm):
    class Meta:
        model=Tweet
        fields=['body']
        
        
class ImageForm(forms.ModelForm):
    class Meta:
        model=Image
        fields=['image']
        widgets={'image':forms.ClearableFileInput(attrs={'muliple':True, 'id':'upload', 'class':'hide'})}
        
class FileForm(forms.ModelForm):
    class Meta:
        model=File
        fields=['file']
        widgets={'file':forms.ClearableFileInput(attrs={'id':'video', 'class':'hide','accept':'application/mp4'})}
       
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['follower', 'user']
