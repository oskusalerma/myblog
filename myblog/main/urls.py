"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from django.contrib.auth import views as auth_views

from . import views, feeds

app_name = "main"

urlpatterns = [
    url(r"^$", views.home, name = "home"),
    url(r"^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$", views.archives, name = "archives"),
    url(r"^login/$", auth_views.login, {"template_name" : "main/login.html"}, name = "login"),
    url(r"^logout/$", auth_views.logout, {"next_page" : "main:home"}, name = "logout"),
    url(r"^new-post/$", views.new_or_edit_post, name = "new-post"),
    url(r"^new-comment/(?P<post_id>[0-9]+)/$", views.new_or_edit_comment, name = "new-comment"),
    url(r"^post/(?P<post_id>[0-9]+)/$", views.post, name = "post"),
    url(r"^post/(?P<post_id>[0-9]+)/edit/$", views.new_or_edit_post, {"is_edit" : True}, name = "edit-post"),
    url(r"^comment/(?P<comment_id>[0-9]+)/edit/$", views.new_or_edit_comment, {"is_edit" : True}, name = "edit-comment"),
    url(r"^feeds/posts/$", feeds.Posts(), name = "feeds-posts"),
    url(r"^feeds/comments/$", feeds.Comments(), name = "feeds-comments"),
]
