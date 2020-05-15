from django.template import RequestContext, Template

from .models import Post

def tags_context(request):
    tag_links = Post.tags.most_common()[:4]
    return {
        'tag_links': tag_links
        }