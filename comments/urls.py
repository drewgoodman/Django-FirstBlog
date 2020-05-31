from django.contrib import admin
from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path('<int:id>/', views.comment_thread, name="comment_thread"),
    path('<int:id>/delete/', views.comment_delete, name="delete_thread"),
    path('user/<int:id>', views.comment_history, name="comment_history")
]
