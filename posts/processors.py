from django.template import RequestContext, Template

from .models import Category, Post

def sidebar_context(request):

    qs_posts = Post.objects.active()
    tag_links = Post.tags.most_common()[:6]
    recent_posts = qs_posts[:4]

    categories = Category.objects.all()

    return {
        'recent_posts': recent_posts,
        'tag_links': tag_links,
        'categories': categories
        }