from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField()

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
        
def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    queryset = Category.objects.filter(slug=slug)
    exists = queryset.exists()
    if exists:
        new_slug = "%s-%s" %(slug, queryset.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Category)