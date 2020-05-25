from django.db import models

class ArchiveManager(models.Manager):
    def with_posts(self, *args, **kwargs):
        return super(ArchiveManager, self).filter(count__gte=1)

class Archive(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    count = models.IntegerField(default=0, null=True, blank=True)
    objects = ArchiveManager()

    def __str__(self):
        return "%s-%s" % (self.date.month,self.date.year)
    
    class Meta:
        verbose_name = "post archive"


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