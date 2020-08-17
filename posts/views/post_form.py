from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View

# Create your views here.
from taggit.models import Tag

from posts.forms import PostForm
from posts.models import Archive, Category, Post
from posts.utils import get_read_time


@login_required
def post_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    if not request.user.is_authenticated:
        raise Http404
    current_date = date.today()
    initial_data = {
        "publish": current_date
    }
    form = PostForm(request.POST or None, request.FILES or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        instance = form.save(commit=False)
        instance.user = request.user
        instance.content = instance.content.strip()
        try:
            blog_img = request.FILES['file']
        except:
            blog_img = None
        if blog_img:
            instance.image = blog_img
        if instance.publish:
            archive_obj, created = Archive.objects.get_or_create(
                date=date(instance.publish.year, instance.publish.month, 1)
                )
            instance.archive = archive_obj
        instance.save()
        form.save_m2m() # required to save tags
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form" : form,
        "full_column" : True,
    }
    return render(request, "post_form.html", context)


@login_required
def post_update(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        try:
            blog_img = request.FILES['file']
        except:
            blog_img = None
        if blog_img:
            instance.image = blog_img
        if instance.publish:
            archive_obj, created = Archive.objects.get_or_create(
                date=date(instance.publish.year, instance.publish.month, 1)
                )
            instance.archive = archive_obj
        instance.save()
        form.save_m2m() # required to save tags
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title" : instance.title,
        "instance" : instance,
        "form": form,
        "full_column" : True,
    }
    return render(request, "post_form.html", context)


@login_required
def post_delete(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted Blog Entry")
    return redirect("posts:home")

