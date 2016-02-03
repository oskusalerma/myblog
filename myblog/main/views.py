from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import BlogInfo, Post
from .forms import PostForm

def home(req):
    bi = BlogInfo.objects.all()[0]
    posts = Post.objects.all().order_by("-pub_date")[:5]

    return render(req, "main/home.html", {"posts" : posts, "blogInfo" : bi})

# TODO: authenticate!
def new_post(req):
    bi = BlogInfo.objects.all()[0]

    if req.method == "POST":
        form = PostForm(req.POST)

        if form.is_valid():
            post = form.save(False)
            post.author = req.user
            post.save()

            return redirect("main:post", post_id = post.pk)

    else:
        form = PostForm()

    return render(req, "main/new_post.html", {"form" : form, "blogInfo" : bi})

def post(req, post_id):
    bi = BlogInfo.objects.all()[0]
    post = get_object_or_404(Post, pk = post_id)

    return render(req, "main/post.html", {"post" : post, "blogInfo" : bi})
