from django.forms import ModelForm, Textarea
from .models import Post, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

        widgets = {
            "content" : Textarea(attrs = { "rows" : 30, "cols" : 80}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content" : Textarea(attrs = { "rows" : 20, "cols" : 80}),
        }
