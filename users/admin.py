from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import Permission


admin.site.register(Profile)
admin.site.register(Permission)
