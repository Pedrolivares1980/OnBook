from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Profile)
admin.site.register(Permission)
