from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name
    
    @property
    def get_posts(self):
        instance = self
        qs = Post.objects.filter_by_instance(instance)
        return qs

    @property
    def get_post_count(self):
        count = 0
        instance = self
        count = len(Post.objects.filter_by_instance(instance))
        return count

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

