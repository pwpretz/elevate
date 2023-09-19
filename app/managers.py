from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, name, cnic):
        if not email:
            raise ValueError(_('Users must have an email address'))
        cnic = self.normalize_email(cnic)
        user = self.model(email=email, name=name, cnic=cnic)
        user.set_password(password)
        user.save()
        return user
