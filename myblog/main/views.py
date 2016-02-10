from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden

from .models import BlogInfo, Post
from .forms import PostForm

def get_ctx(archives = True):
    return {
        "blog_info" : BlogInfo.objects.all()[0],
        "archives" : archives and get_archives() or None,
        "my_date_format" : "F j, Y, H:i",
        }

def home(req):
    ctx = get_ctx()
    ctx["posts"] = Post.objects.all().order_by("-pub_date")[:5]

    return render(req, "main/home.html", ctx)

def archives(req, year, month):
    ctx = get_ctx()

    ctx["posts"] = (
        Post.objects
        .filter(pub_date__year = year)
        .filter(pub_date__month = month)
        .order_by("-pub_date"))

    return render(req, "main/home.html", ctx)

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

    ctx = get_ctx(archives = False)
    ctx["form"] = form
    ctx["post"] = post

    return render(req, "main/new_post.html", ctx)

def post(req, post_id):
    ctx = get_ctx()

    ctx["post"] = get_object_or_404(Post, pk = post_id)

    return render(req, "main/post.html", ctx)

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
