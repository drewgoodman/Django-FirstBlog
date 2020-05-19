from django.template import RequestContext, Template

from .models import Post

def sidebar_context(request):

    qs_posts = Post.objects.active()
    tag_links = Post.tags.most_common()[:6]
    recent_posts = qs_posts[:4]

    # archive_list = []

    # for post in qs_posts:
    #     date = "%s-%s" % (post.publish.month,post.publish.year)
    #         if date in archive_list.values():
    #             archive_list['count'] += 1
    #             break
    #         else:
    #             archive_month = {
    #                 "date": date,
    #                 "month": post.publish.month,
    #                 "year": post.publish.year,
    #                 "count": count
    #             }
    #             archive_list.append(archive_month)
    # print(archive_list)

    return {
        'recent_posts': recent_posts,
        'tag_links': tag_links,
        # 'archive_list': archive_list,
        }