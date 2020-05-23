from django.contrib import admin
from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    # path('<int:post_id>', views.post_home),
    path('', views.post_home, name="home"),
    path('posts/', views.post_list, name="list"),
    path('posts/category/<slug>/', views.post_list, name="category_view"),
    path('posts/tag/<slug>/', views.post_list, name="tag_view"),
    path('create/', views.post_create, name="create"),
    path('posts/<slug>/', views.PostListView.as_view(), name="detail"),
    path('posts/<slug:slug>/edit/', views.post_update, name="update"),
    path('posts/<slug:slug>/delete/', views.post_delete),

]
