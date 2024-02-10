from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentReplyView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="blog-home" ),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"), 
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"), 
    path("post/<int:pk>/comment/", CommentCreateView.as_view(), name="add-comment"),
    path("post/<int:post_id>/comment/<int:parent_id>/reply/", CommentReplyView.as_view(), name="add-reply"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
]
