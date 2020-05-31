import calendar

from datetime import date
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View

from taggit.models import Tag

from posts.models import Archive, Category, Post



def post_home(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active_img()[:3]
    pinned_qs = Post.objects.pinned()
    context = {
        "object_list" : queryset_list,
        "pinned_posts": pinned_qs,
        "title" : "Post List",
        "today" : today,
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