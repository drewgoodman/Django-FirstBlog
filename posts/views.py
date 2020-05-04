from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect

from urllib.parse import quote_plus

# Create your views here.
from .models import Post
from .forms import PostForm

# Function based views vs class based views

def post_create(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        # print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form" : form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, slug=slug)
    share_string = quote_plus(instance.content)
    context = {
        "title" : instance.title,
        "instance" : instance,
        "share_string" : share_string
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 10) # Show 10 posts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "object_list" : page_obj,
        "title" : "Post List"
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title" : instance.title,
        "instance" : instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted Blog Entry")
    return redirect("posts:list")

