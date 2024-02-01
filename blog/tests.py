from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment


class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.post = Post.objects.create(
            author=cls.user, title="Test Post", content="This is a test post"
        )

    def test_post_content(self):
        post = Post.objects.get(id=1)
        expected_author = f"{post.author}"
        expected_title = f"{post.title}"
        expected_content = f"{post.content}"
        self.assertEqual(expected_author, "testuser")
        self.assertEqual(expected_title, "Test Post")
        self.assertEqual(expected_content, "This is a test post")

    def test_post_str_method(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), post.title)

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEqual(
            post.get_absolute_url(), reverse("post-detail", args=[post.id])
        )


class PostViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(
            author=self.user, title="Test Post", content="This is a test post"
        )

    def test_post_list_view(self):
        url = reverse("blog-home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test post")
        self.assertTemplateUsed(response, "blog/home.html")

    def test_post_detail_view(self):
        url = reverse("post-detail", args=[self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_create_post_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("post-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

        response = self.client.post(
            reverse("post-create"),
            {
                "title": "New title",
                "content": "New text",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(Post.objects.filter(title="New title").exists())

    def test_update_post_view(self):
        self.client.login(username="testuser", password="12345")
        url = reverse("post-update", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

        response = self.client.post(
            url,
            {
                "title": "Updated title",
                "content": "Updated text",
            },
        )
        self.post.refresh_from_db()
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertEqual(self.post.title, "Updated title")

    def test_update_post_view_unauthorized(self):
        """Test that an unauthorized user cannot update a post."""
        other_user = User.objects.create_user(username="otheruser", password="12345")
        self.client.login(username="otheruser", password="12345")
        url = reverse("post-update", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.post(
            url, {"title": "Unauthorized Update", "content": "Should not happen"}
        )
        self.post.refresh_from_db()
        self.assertNotEqual(self.post.title, "Unauthorized Update")

    def test_delete_post_view(self):
        self.client.login(username="testuser", password="12345")
        url = reverse("post-delete", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_confirm_delete.html")

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_delete_post_view_unauthorized(self):
        """Test that an unauthorized user cannot delete a post."""
        other_user = User.objects.create_user(username="otheruser", password="12345")
        self.client.login(username="otheruser", password="12345")
        url = reverse("post-delete", kwargs={"pk": self.post.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())


class CommentModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="commentuser", password="12345")
        cls.post = Post.objects.create(
            author=cls.user,
            title="Test Post for Comment",
            content="This is a test post for a comment",
        )
        cls.comment = Comment.objects.create(
            post=cls.post, author=cls.user, content="This is a test comment"
        )

    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        expected_author = f"{comment.author}"
        expected_post = f"{comment.post}"
        expected_content = f"{comment.content}"
        self.assertEqual(expected_author, "commentuser")
        self.assertEqual(expected_post, "Test Post for Comment")
        self.assertEqual(expected_content, "This is a test comment")

    def test_comment_str_method(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(
            str(comment),
            f"Comment by {comment.author.username} on {comment.post.title}",
        )

    def test_get_absolute_url(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(
            comment.get_absolute_url(), reverse("post-detail", args=[comment.post.id])
        )


class CommentViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="commentuser", password="12345")
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post for Comment",
            content="This is a test post for a comment",
        )

    def test_add_comment_view(self):
        self.client.login(username="commentuser", password="12345")
        url = reverse("add-comment", kwargs={"pk": self.post.pk})
        response = self.client.post(url, {"content": "New Comment"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content="New Comment").exists())


class CommentReplyViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="replyuser", password="12345")
        self.other_user = User.objects.create_user(
            username="otheruser", password="12345"
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post for Reply",
            content="This is a test post for a reply",
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, content="This is a test comment"
        )

    def test_add_reply_to_comment_view(self):
        self.client.login(username="replyuser", password="12345")
        url = reverse(
            "add-reply", kwargs={"post_id": self.post.pk, "parent_id": self.comment.pk}
        )
        response = self.client.post(url, {"content": "New Reply"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Comment.objects.filter(content="New Reply", parent=self.comment).exists()
        )


class CommentUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="updateuser", password="12345")
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post for Comment Update",
            content="This is a test post for comment update",
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, content="This is a test comment"
        )

    def test_update_comment_view(self):
        self.client.login(username="updateuser", password="12345")
        url = reverse("comment-update", kwargs={"pk": self.comment.pk})
        response = self.client.post(url, {"content": "Updated Comment"})
        self.assertEqual(response.status_code, 302)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, "Updated Comment")

    def test_update_comment_view_unauthorized(self):
        """Test that an unauthorized user cannot update a comment."""
        other_user = User.objects.create_user(username="otheruser", password="12345")
        self.client.login(username="otheruser", password="12345")
        url = reverse("comment-update", kwargs={"pk": self.comment.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.post(url, {"content": "Unauthorized Update"})
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content, "Unauthorized Update")


class CommentDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="deleteuser", password="12345")
        self.post = Post.objects.create(
            author=self.user,
            title="Test Post for Comment Delete",
            content="This is a test post for comment delete",
        )
        self.parent_comment = Comment.objects.create(
            post=self.post, author=self.user, content="This is a parent test comment"
        )
        self.child_comment = Comment.objects.create(
            post=self.post, author=self.user, content="This is a child test comment", parent=self.parent_comment
        )

    def test_recursive_delete_comment_view(self):
        """Test that deleting a comment also deletes its child comments."""
        self.client.login(username="deleteuser", password="12345")
        url = reverse("comment-delete", kwargs={"pk": self.parent_comment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=self.parent_comment.pk).exists())
        self.assertFalse(Comment.objects.filter(pk=self.child_comment.pk).exists())

    def test_delete_comment_view_unauthorized(self):
        """Test that an unauthorized user cannot delete a comment."""
        other_user = User.objects.create_user(username="otheruser", password="12345")
        self.client.login(username="otheruser", password="12345")
        url = reverse("comment-delete", kwargs={"pk": self.parent_comment.pk})
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        response = self.client.post(url)
        self.assertTrue(Comment.objects.filter(pk=self.parent_comment.pk).exists())