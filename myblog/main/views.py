from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden

from .models import BlogInfo, Post
from .forms import PostForm

def home(req):
    bi = BlogInfo.objects.all()[0]
    posts = Post.objects.all().order_by("-pub_date")[:5]

    return render(req, "main/home.html", {
        "posts" : posts, "blogInfo" : bi, "archives" : get_archives()})

def archives(req, year, month):
    bi = BlogInfo.objects.all()[0]

    posts = (Post.objects
             .filter(pub_date__year = year)
             .filter(pub_date__month = month)
             .order_by("-pub_date"))

    return render(req, "main/home.html", {
        "posts" : posts, "blogInfo" : bi, "archives" : get_archives()})

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

    return render(req, "main/post.html", {
        "post" : post, "blogInfo" : bi, "archives" : get_archives()})

def get_archives():
    posts = Post.objects.all().order_by("-pub_date")
    ret = []

    for i, post in enumerate(posts):
        if (i > 0) and ((posts[i - 1].pub_date.year == post.pub_date.year) and
                        (posts[i - 1].pub_date.month == post.pub_date.month)):
            ret[-1]["nr_of_posts"] += 1
        else:
            ret.append({
                "month" : post.pub_date.strftime("%m"),
                "month_name" : post.pub_date.strftime("%B"),
                "year" : post.pub_date.year,
                "nr_of_posts" : 1})

    return ret
