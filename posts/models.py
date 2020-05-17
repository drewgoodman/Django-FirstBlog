from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

# Third Party
from markdown_deux import markdown
from taggit.managers import TaggableManager

from comments.models import Comment

from .utils import get_read_time


class PostManager(models.Manager):
    #Post.objects.all() = super(postManager, self).all()
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
    
    def active_img(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now()).exclude(image="")


def upload_location(instance, filename):
    return "blog/%s/%s" %(instance.id, filename)
    # base for modifying image name:
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    
    image = models.ImageField(upload_to=upload_location,
            null=True, blank=True, 
            width_field="width_field",
            height_field="height_field")
    height_field = models.IntegerField(default=0, null=True, blank=True)
    width_field = models.IntegerField(default=0, null=True, blank=True)
    
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    
    tags = TaggableManager(blank=True)

    read_time = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = PostManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"slug":self.slug})
        # return "/posts/%s/" %(self.id)

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def comment_count(self): #includes all child comments in threads
        count = 0
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        for comment in qs:
            count += 1
            child_qs = Comment.objects.filter(parent=comment)
            count += len(child_qs)
        return count

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    
    class Meta:
        ordering = ["-publish","-timestamp","-updated"]


# recursive function required since otherwise the Id will be = None when attempting to create a unique slug
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    queryset = Post.objects.filter(slug=slug)
    exists = queryset.exists()
    if exists:
        new_slug = "%s-%s" %(slug, queryset.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time = get_read_time(html_string)
        instance.read_time = read_time

pre_save.connect(pre_save_post_receiver, sender=Post)