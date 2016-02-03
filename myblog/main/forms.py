from django.forms import ModelForm, Textarea
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

        widgets = {
            "content" : Textarea(attrs = { "rows" : 30, "cols" : 80}),
        }
