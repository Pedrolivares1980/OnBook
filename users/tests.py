from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile
import os

class UserTestCase(TestCase):
    def setUp(self):
        # Create a test user and an admin user for testing
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@example.com', password='adminpassword')
        
        # Create or get profiles for these users
        Profile.objects.get_or_create(user=self.user)
        Profile.objects.get_or_create(user=self.admin_user)

    def test_register_user(self):
        # Test user registration process
        response = self.client.post(reverse('register'), {'username': 'newuser', 'email': 'newuser@example.com', 'password1': 'newpassword123', 'password2': 'newpassword123'})
        self.assertEqual(response.status_code, 302)  # Expect redirection after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_profile_update(self):
        # Test updating a user's profile
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(reverse('edit_profile'), {'username': 'updateduser', 'email': 'updateduser@example.com'})
        self.assertEqual(response.status_code, 302)  # Expect redirection after successful update
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_user_profile_picture_upload(self):
        # Test uploading a profile picture
        self.client.login(username='testuser', password='password')
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('edit_profile'), {'username': self.user.username, 'email': self.user.email, 'image': image})
        self.assertEqual(response.status_code, 200)  # Expect successful response instead of redirection



    def test_user_profile_picture_update(self):
        # Test updating a user's profile picture
        self.client.login(username='testuser', password='password')
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg").name
        with open(temp_file, 'wb') as img:
            Image.new('RGB', (100, 100)).save(img, 'JPEG')
        with open(temp_file, 'rb') as img:
            response = self.client.post(reverse('edit_profile'), {'username': self.user.username, 'email': self.user.email, 'image': img})
        os.remove(temp_file)
        self.assertEqual(response.status_code, 302)  # Expect redirection after successful update


    def test_admin_views_access(self):
        # Test admin's access to admin-specific views
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('admin_users'))
        self.assertEqual(response.status_code, 200)  # Admin should have access

    def test_admin_edit_user(self):
        # Test admin editing a user's information
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.post(reverse('edit_user', args=[self.user.id]), {'username': 'editeduser', 'email': 'editeduser@example.com'})
        self.assertEqual(response.status_code, 302)  # Expect redirection after successful edit
        edited_user = User.objects.get(id=self.user.id)
        self.assertEqual(edited_user.username, 'editeduser')

    def test_admin_delete_user(self):
        # Test admin deleting a user
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.post(reverse('delete_user', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Expect redirection after successful deletion
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_non_admin_access_restricted_views(self):
        # Test that non-admin users cannot access admin-only views
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('admin_users'))
        self.assertNotEqual(response.status_code, 200)  # Non-admin should not have access

    def test_user_detail_view_by_admin(self):
        # Test admin viewing a user's detail
        self.client.login(username='adminuser', password='adminpassword')
        response = self.client.get(reverse('user_detail', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)  # Admin should be able to access user detail view

    # Add more tests as needed...
