from django.contrib.auth.backends import BaseBackend
from django.conf import settings

class UserAuth(BaseBackend):
    def has_perm(self, user_obj, perm, obj):
        return user_obj.username == settings.ADMIN_LOGIN
        # return super().has_perm(user_obj, perm, obj=obj)