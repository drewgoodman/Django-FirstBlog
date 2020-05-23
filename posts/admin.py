from django.contrib import admin, messages
from django.utils.translation import ngettext

# Register your models here.
# from posts.models import Post
from .models import Archive, Category, Post #relative import

class PostModelAdmin(admin.ModelAdmin):

    list_display = ["title", "timestamp", "updated","draft"]
    list_display_links = ["updated"] #change which field has a link to change the entry
    list_editable = ["title","draft"]

    list_filter = ["updated", "timestamp","draft"] #create options to sort by these fields
    search_fields= ["title","content"] #allow for searching in these fields
    actions = ["make_published", "make_draft"]

    class Meta:
        model = Post

    def make_published(self, request, queryset):
        updated = queryset.update(draft=False)
        self.message_user(request, ngettext(
            '%d story was marked as published.',
            '%d stories were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)
    make_published.short_description = "Mark as Published"

    def make_draft(self, request, queryset):
        updated = queryset.update(draft=True)
        self.message_user(request, ngettext(
            '%d story was marked as draft.',
            '%d stories were successfully marked as draft.',
            updated,
        ) % updated, messages.SUCCESS)
    make_draft.short_description = "Mark as Draft"


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        model = Category

class ArchiveModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Archive

admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Archive, ArchiveModelAdmin)

