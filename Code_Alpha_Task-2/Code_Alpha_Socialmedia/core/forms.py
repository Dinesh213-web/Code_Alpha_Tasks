from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    """
    Handles text + optional image/video uploads.
    The template must include enctype="multipart/form-data" on the <form> tag,
    and the view must pass request.FILES when instantiating this form.
    """
    class Meta:
        model = Post
        fields = ['content', 'image', 'video']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': "What's on your mind? (optional if uploading media)",
                'rows': 3,
            }),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'video': forms.ClearableFileInput(attrs={'accept': 'video/*'}),
        }
        labels = {
            'content': '',
            'image': '📷 Image (optional)',
            'video': '🎥 Video (optional)',
        }

    def clean(self):
        """At least one of content, image, or video must be provided."""
        cleaned = super().clean()
        if not cleaned.get('content') and not cleaned.get('image') and not cleaned.get('video'):
            raise forms.ValidationError("Please add some text, an image, or a video.")
        return cleaned


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Write a comment...',
            })
        }
        labels = {
            'content': ''
        }
