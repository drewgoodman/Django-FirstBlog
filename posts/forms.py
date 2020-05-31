from datetime import date

from django import forms
from pagedown.widgets import PagedownWidget
from django.utils.translation import gettext_lazy as _

from .models import Post

current_year = date.today().year
PUBLISH_YEAR_RANGE = list(range(current_year-1,current_year+8))


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(widget=forms.SelectDateWidget(years=PUBLISH_YEAR_RANGE))
    class Meta:
        model = Post
        fields = (
            "title",
            "image",
            "content",
            "category",
            "draft",
            "pinned",
            "publish",
            "tags",
        )
        labels = {
            "title": _("Blog Title"),
            "pinned": _("Pin on Homepage?"),
            "image": _("Cover Image"),
            "publish": _("Publishing Date"),
            "draft": _("Set as Draft")
        }