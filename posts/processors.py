from django.template import RequestContext, Template

from .models import Post

def sidebar_context(request):
    
    recent_posts = Post.objects.active()[:4]
    tag_links = Post.tags.most_common()[:6]
    return {
        'recent_posts': recent_posts,
        'tag_links': tag_links,
        }