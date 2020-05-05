from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "image",
            "draft",
            "publish"
        )
        labels = {
            "title": _("Blog Title"),
            "image": _("Cover Image"),
            "publish": _("Publishing Date"),
            "draft": _("Set as Draft")
        }