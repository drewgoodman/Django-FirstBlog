from django.contrib import admin
from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    # path('<int:post_id>', views.post_home),
    path('', views.post_list),
    path('create/', views.post_create),
    path('<int:id>/', views.post_detail, name="detail"),
    path('update/', views.post_update),
    path('delete/', views.post_delete),

]
