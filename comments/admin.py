from django.contrib import admin

# from posts.models import Post
from .models import Comment

class CommentModelAdmin(admin.ModelAdmin):

    list_display = ["user","content","timestamp"]

    list_display_links = ["timestamp"] #change which field has a link to change the entry
    # list_editable = ["content"]

    list_filter = ["user", "timestamp"] #create options to sort by these fields
    search_fields= ["content"] #allow for searching in these fields

    class Meta:
        model = Comment

admin.site.register(Comment, CommentModelAdmin)