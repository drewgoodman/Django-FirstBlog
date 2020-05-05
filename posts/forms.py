from django import forms
from pagedown.widgets import PagedownWidget
from django.utils.translation import gettext_lazy as _

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(widget=forms.SelectDateWidget)
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