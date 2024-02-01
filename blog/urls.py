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
    path(
        "", PostListView.as_view(), name="blog-home"
    ),  # Home page showing list of posts
    path(
        "post/<int:pk>/", PostDetailView.as_view(), name="post-detail"
    ),  # Detail view of a specific post
    path(
        "post/new/", PostCreateView.as_view(), name="post-create"
    ),  # Page to create a new post
    path(
        "post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"
    ),  # Update a specific post
    path(
        "post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"
    ),  # Delete a specific post
    path(
        "post/<int:pk>/comment/", CommentCreateView.as_view(), name="add-comment"
    ),  # Add a comment to a post
    path(
        "post/<int:post_id>/comment/<int:parent_id>/reply/",
        CommentReplyView.as_view(),
        name="add-reply",
    ),  # Reply to a specific comment
    path(
        "comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"
    ),  # Update a specific comment
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),  # Delete a specific comment
]
