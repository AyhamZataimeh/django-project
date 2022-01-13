from django.contrib import admin
from .models import UserAccount, Products, ProfileImage, BlockUsers, RequestedBook

admin.site.register(UserAccount)
admin.site.register(Products)
admin.site.register(ProfileImage)
admin.site.register(BlockUsers)
admin.site.register(RequestedBook)


# Register your models here.
