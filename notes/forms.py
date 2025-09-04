from django import forms
from .models import Note , UserProfile  # ✅ Capital N

class Noteform(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'attachment']
        widgets = {
            'title': forms.TextInput(attrs={'autofocus': 'autofocus'}),
            'content': forms.Textarea(attrs={'rows': 4}),
        }
        
class Userprofileform(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_pic"]
