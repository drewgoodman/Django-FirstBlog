import calendar

from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from urllib.parse import quote_plus

# Create your views here.
from comments.forms import CommentForm
from comments.models import Comment
from taggit.models import Tag

from .forms import PostForm
from .models import Archive, Category, Post
from .utils import get_read_time



def post_home(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active_img()[:3]
    context = {
        "object_list" : queryset_list,
        "title" : "Post List",
        "today" : today
    }
    return render(request, "home.html", context)


class PostListView(View):
    
    title = "Post List"

    def update_title(self, queryset, title_base, filter_name):
        count = len(queryset)
        if count == 1:
            results_str = "result"
        else:
            results_str = "results"
        self.title = "%s: %s -- (%s %s)" % (title_base, filter_name, count, results_str)

    def paginate_list(self, queryset, page_number, max_posts):
        paginator = Paginator(queryset, max_posts)
        return paginator.get_page(page_number)

    def filter_by_slug(self, queryset_list, slug):
        pass #placeholder -- define in query Class Views

    def filter_by_query(self, queryset_list, query):
        filtered_queryset = queryset_list.filter(
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query) |
                    Q(tags__name__in=[query])
                    ).distinct()
        return filtered_queryset

    def get(self, request, slug=None, slug_year=None):
        
        today = timezone.now().date()

        if request.user.is_authenticated:
            queryset_list = Post.objects.all()
        else:
            queryset_list = Post.objects.active()

        if slug:
            queryset_list = self.filter_by_slug(queryset_list, slug, slug_year)
        else:
            query = request.GET.get("query")
            if query:
                queryset_list = self.filter_by_query(queryset_list, query)
                self.update_title(queryset_list,"Search results for",query)

        page_number = request.GET.get('page')
        page_obj = self.paginate_list(queryset_list, page_number, 10)

        context = {
            "object_list" : page_obj,
            "title" : self.title,
            "today" : today
        }
        return render(request, "post_list.html", context)


class PostTagView(PostListView):
    title = "Filter By Tag: " 

    def filter_by_slug(self, queryset_list, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        filtered_queryset = queryset_list.filter(tags=tag)
        self.update_title(filtered_queryset,"Tag",tag)
        return filtered_queryset


class PostCategoryView(PostListView):
    title = "Filter By Category: "

    def filter_by_slug(self, queryset_list, slug, *args, **kwargs):
        category = get_object_or_404(Category, slug=slug)
        filtered_queryset = queryset_list.filter(category=category)
        self.update_title(filtered_queryset,"Category",category.name)
        return filtered_queryset


class PostArchiveView(PostListView):
    title = "Articles from "

    def filter_by_slug(self, queryset_list, slug, slug_year, *args, **kwargs):
        year = int(slug_year)
        month = int(slug)
        archive_date = date(year, month, 1)
        archive = get_object_or_404(Archive, date=archive_date)
        filtered_queryset = queryset_list.filter(archive=archive)
        self.title = "Articles from " + calendar.month_name[month] + " " + str(year)
        return filtered_queryset


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

