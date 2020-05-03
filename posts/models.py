from django.db import models
from django.urls import reverse
# Create your models here.
# MVC MODEL VIEW CONTROLLER

class Post(models.Model):
    title = models.CharField(max_length=120)
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