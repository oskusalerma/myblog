import collections

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden
from django.core.cache import cache
from django.db.models import Q

from .models import BlogInfo, Post, Comment
from .forms import PostForm, CommentForm

# cache key
BI_KEY = "BlogInfo"

def get_ctx(archives = True):
    bi = cache.get(BI_KEY)

    if not bi:
        bi = BlogInfo.objects.all()[0]
        cache.set(BI_KEY, bi)

    return {
        "blog_info" : bi,
        "archives" : archives and get_archives() or None,
        "my_date_format" : "F j, Y, H:i",
        }

def add_nr_of_comments(posts):
    postIds = [post.pk for post in posts]

    # TODO: this is the SQL query I'd like to do:
    #
    # select count(*),post_id
    # from main_comment
    # where post_id in (postIds)
    # group by post_id;
    #
    # but I don't know yet how to do that in the Django ORM.

    comments = Comment.objects.filter(post_id__in = postIds).values_list("post_id", flat = True)
    commentsPerPost = collections.defaultdict(int)

    for postId in comments:
        commentsPerPost[postId] += 1

    for post in posts:
        post.nr_of_comments = commentsPerPost[post.pk]

    return posts

def home(req):
    ctx = get_ctx()
    ctx["posts"] = add_nr_of_comments(Post.objects.select_related("author").all().order_by("-pub_date")[:5])

    return render(req, "main/home.html", ctx)

def archives(req, year, month):
    ctx = get_ctx()

    ctx["posts"] = add_nr_of_comments(
        Post.objects
        .select_related("author")
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

def new_or_edit_comment(req, post_id = None, comment_id = None, is_edit = False):
    if is_edit:
        comment = get_object_or_404(Comment, pk = comment_id)
        post_id = comment.post.pk
        allow = (comment.author == req.user) or req.user.is_superuser
    else:
        comment = None
        allow = req.user.is_authenticated()

    if not allow:
        return HttpResponseForbidden("forbidden")

    if req.method == "POST":
        form = CommentForm(req.POST, instance = comment)

        if form.is_valid():
            newComment = form.save(False)

            if not is_edit:
                newComment.author = req.user
                newComment.post = get_object_or_404(Post, pk = post_id)

            newComment.save()

            url = "%s#comment_%s" % (
                reverse("main:post", kwargs = {"post_id" : post_id}),
                newComment.pk)

            return redirect(url)

    else:
        form = CommentForm(instance = comment)

    ctx = get_ctx(archives = False)
    ctx["form"] = form
    ctx["comment"] = comment
    ctx["post_id"] = post_id

    return render(req, "main/new_comment.html", ctx)

def post(req, post_id):
    ctx = get_ctx()

    post = get_object_or_404(Post.objects.select_related("author"), pk = post_id)
    comments = Comment.objects.select_related("author").filter(post_id = post_id).order_by("pub_date")
    post.nr_of_comments = len(comments)

    ctx["post"] = post
    ctx["comments"] = comments
    ctx["show_comments"] = True

    return render(req, "main/post.html", ctx)

def search(req):
    ctx = get_ctx()

    query = req.GET.get("q")
    ctx["query"] = query

    if query:
        ctx["posts"] = (
            Post.objects
            .filter(
                Q(title__icontains = query) |
                Q(content__icontains = query))
            .order_by("-pub_date"))

    return render(req, "main/search_results.html", ctx)

def get_archives():
    # TODO: this SQL query would get what I want in one query without
    # having to manually go through each post, but I don't know yet how to
    # achieve it it Django's ORM:
    #
    # select count(*),
    #  extract('year' from pub_date) as year,
    #  extract('month' from pub_date) as month
    # from main_post
    # group by extract('year' from pub_date),
    #  extract('month' from pub_date);

    posts = Post.objects.all().order_by("-pub_date").values_list("pub_date", flat = True)
    ret = []

    for i, post in enumerate(posts):
        if (i > 0) and ((posts[i - 1].year == post.year) and
                        (posts[i - 1].month == post.month)):
            ret[-1]["nr_of_posts"] += 1
        else:
            ret.append({
                "month" : post.strftime("%m"),
                "month_name" : post.strftime("%B"),
                "year" : post.year,
                "nr_of_posts" : 1})

    return ret
