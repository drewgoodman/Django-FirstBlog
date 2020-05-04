from django.contrib import admin

# Register your models here.
# from posts.models import Post
from .models import Post #relative import

class PostModelAdmin(admin.ModelAdmin):

    list_display = ["title", "timestamp", "updated","draft"]
    list_display_links = ["updated"] #change which field has a link to change the entry
    list_editable = ["title","draft"]

    list_filter = ["updated", "timestamp","draft"] #create options to sort by these fields
    search_fields= ["title","content"] #allow for searching in these fields

    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)

