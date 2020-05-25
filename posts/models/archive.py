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
        ordering = ["-date"]