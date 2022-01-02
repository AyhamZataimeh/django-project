from django.contrib import admin
from .models import UserAccount, Products, ProfileImage, BlockUsers

admin.site.register(UserAccount)
admin.site.register(Products)
admin.site.register(ProfileImage)
admin.site.register(BlockUsers)

# Register your models here.
