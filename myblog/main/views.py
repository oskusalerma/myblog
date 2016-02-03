from django.shortcuts import render
from django.http import HttpResponse

from .models import BlogInfo, Post

def home(req):
    bi = BlogInfo.objects.all()[0]
    posts = Post.objects.all().order_by("-pub_date")[:5]

    return render(req, "main/home.html", {"posts" : posts, "blogInfo" : bi})
