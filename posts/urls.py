from django.contrib import admin
from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    # path('<int:post_id>', views.post_home),
    path('', views.post_home, name="home"),
    path('posts/', views.PostListView.as_view(), name="list"),
    path('posts/category/<slug>/', views.PostCategoryView.as_view(), name="category_view"),
    path('posts/tag/<slug>/', views.PostTagView.as_view(), name="tag_view"),
    path('create/', views.post_create, name="create"),
    path('posts/<slug>/', views.post_detail, name="detail"),
    path('posts/<slug:slug>/edit/', views.post_update, name="post_update"),
    path('posts/<slug:slug>/delete/', views.post_delete, name="post_delete"),
    path('posts/archive/<slug:slug_year>/<slug:slug>/', views.PostArchiveView.as_view(), name="archive_view"),

]
