from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden

from .models import BlogInfo, Post
from .forms import PostForm

def home(req):
    bi = BlogInfo.objects.all()[0]
    posts = Post.objects.all().order_by("-pub_date")[:5]

    return render(req, "main/home.html", {"posts" : posts, "blogInfo" : bi})

def new_or_edit_post(req, post_id = None, is_edit = False):
    if is_edit:
        post = get_object_or_404(Post, pk = post_id)
        allow = (post.author == req.user) or req.user.is_superuser
    else:
        post = None
        allow = req.user.is_authenticated()

    if not allow:
        return HttpResponseForbidden("forbidden")

    bi = BlogInfo.objects.all()[0]

    if req.method == "POST":
        form = PostForm(req.POST, instance = post)

        if form.is_valid():
            newPost = form.save(False)

            if not is_edit:
                newPost.author = req.user

            newPost.save()

            return redirect("main:post", post_id = newPost.pk)

    else:
        form = PostForm(instance = post)

    return render(req, "main/new_post.html", {"form" : form, "blogInfo" : bi, "post" : post})

def post(req, post_id):
    bi = BlogInfo.objects.all()[0]
    post = get_object_or_404(Post, pk = post_id)

    return render(req, "main/post.html", {"post" : post, "blogInfo" : bi})
