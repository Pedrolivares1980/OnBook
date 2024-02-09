from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django import forms


import logging

logger = logging.getLogger(__name__)


def home(request):
    """View to render the home page with a list of posts."""
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    """View to display a list of blog posts."""

    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]


class PostDetailView(DetailView):
    """View to display the details of a specific blog post, including its main comments."""

    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main_comments"] = Comment.objects.filter(
            post=self.get_object(), parent__isnull=True
        ).order_by("-date_posted")
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """View to create a new blog post."""

    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View to update an existing blog post."""

    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete a blog post."""

    model = Post
    success_url = reverse_lazy("blog-home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentCreateView(LoginRequiredMixin, CreateView):
    """View to create a new comment on a blog post."""

    model = Comment
    fields = ["content"]
    template_name = "blog/add_comment.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = forms.Textarea(attrs={
            'rows': 8,
            'style': 'resize:none;',  
            'placeholder': 'Write your comment here...'
        })
        form.fields['content'].label = ''
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['post_detail'] = {
            'author_profile_image': post.author.profile.image.url,
            'author_username': post.author.username,
            'date_posted': post.date_posted,
            'title': post.title,
            'content': post.content
        }
        return context


class CommentReplyView(LoginRequiredMixin, CreateView):
    """View to create a reply to a comment."""

    model = Comment
    fields = ["content"]
    template_name = "blog/add_reply.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = forms.Textarea(attrs={
            'rows': 8,
            'style': 'resize:none;',  
            'placeholder': 'Write your comment here...'
        })
        form.fields['content'].label = ''
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.parent_id = self.kwargs["parent_id"]
        form.instance.post_id = self.kwargs["post_id"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["post_id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['parent_id'])
        context['parent_comment'] = parent_comment
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["content"]
    template_name = "blog/comment_update.html"  # Crear este template

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        """
        Ensure only the comment author can delete the comment.
        """
        comment = self.get_object()
        if self.request.user != comment.author:
            raise PermissionDenied("You are not allowed to delete this comment.")
        return True

    def get_success_url(self):
        """
        Redirect to the associated post's detail page after deletion.
        """
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def form_valid(self, form):
        """
        Overridden to handle recursive deletion of comments.
        """
        comment = self.get_object()
        try:
            self._recursive_delete(comment)
        except Exception as e:
            logger.error(f"Error occurred while deleting comment {comment.id}: {e}", exc_info=True)

        return super().form_valid(form)

    def _recursive_delete(self, comment):
        """
        Recursively delete child comments before deleting the comment itself.
        """
        for child_comment in comment.replies.all():
            self._recursive_delete(child_comment)
        comment.delete()