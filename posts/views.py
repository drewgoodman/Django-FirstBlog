from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
from .models import Post
from .forms import PostForm

# Function based views vs class based views

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form" : form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    # instance = Post.objects.get(id=1)
    instance = get_object_or_404(Post, id=id)
    context = {
        "title" : instance.title,
        "instance" : instance
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset = Post.objects.all()
    context = {
        "object_list" : queryset,
        "title" : "List"
    }
    return render(request, "index.html", context)


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title" : instance.title,
        "instance" : instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request):
    return HttpResponse("<h1>delete</h1>")

