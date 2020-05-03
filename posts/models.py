from django.db import models
from django.urls import reverse
# Create your models here.
# MVC MODEL VIEW CONTROLLER

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)
    # base for modifying image name:
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)


class Post(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location,
            null=True, blank=True, 
            width_field="width_field",
            height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"id":self.id})
        # return "/posts/%s/" %(self.id)
    
    class Meta:
        ordering = ["-timestamp","-updated"]