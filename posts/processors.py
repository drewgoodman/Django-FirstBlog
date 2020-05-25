from django.template import RequestContext, Template

from .models import Archive, Category, Post

def sidebar_context(request):

    qs_posts = Post.objects.active()
    tag_links = Post.tags.most_common()[:6]
    recent_posts = qs_posts[:4]

    categories = Category.objects.all()
    archives = Archive.objects.with_posts()

    return {
        'recent_posts': recent_posts,
        'tag_links': tag_links,
        'archives': archives,
        'categories': categories,
        }