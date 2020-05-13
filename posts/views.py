from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from urllib.parse import quote_plus

# Create your views here.
from comments.forms import CommentForm
from comments.models import Comment

from .forms import PostForm
from .models import Post
from .utils import get_read_time

# Function based views vs class based views

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
        instance.save()
        form.save_m2m() # required to save tags
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form" : form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_authenticated:
            raise Http404
    share_string = quote_plus(instance.content)
    initial_data = {
        "content_type": instance.get_content_type.model,
        "object_id": instance.id,
    }

    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type = content_type,
            object_id = obj_id,
            content = content_data,
            parent = parent_obj,
        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    comments = instance.comments
    context = {
        "title" : instance.title,
        "instance" : instance,
        "share_string" : share_string,
        "comments" : comments,
        "comment_form": form
    }
    return render(request, "post_detail.html", context)

def post_home(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()[:3]
    context = {
        "object_list" : queryset_list,
        "title" : "Post List",
        "today" : today
    }
    return render(request, "home.html", context)

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    # queryset_list = Post.objects.all()
    if request.user.is_authenticated:
        queryset_list = Post.objects.all()
    query = request.GET.get("query")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset_list, 2) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "object_list" : page_obj,
        "title" : "Post List",
        "today" : today
    }
    return render(request, "post_list.html", context)

@login_required
def post_update(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m() # required to save tags
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags="html_safe")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title" : instance.title,
        "instance" : instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


@login_required
def post_delete(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Deleted Blog Entry")
    return redirect("posts:list")

