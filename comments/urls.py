from django.contrib import admin
from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path('<int:id>/', views.comment_thread, name="comment_thread"),
    # path('<slug:slug>/delete/', views.comment_delete),

]
