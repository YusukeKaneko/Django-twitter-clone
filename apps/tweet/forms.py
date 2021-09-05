from django import forms

from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content')
        widgets = {
            'content': forms.Textarea(
                attrs={'rows': 10, 'cols': 30, 'placeholder': 'ここに入力'}
            ),
        }
