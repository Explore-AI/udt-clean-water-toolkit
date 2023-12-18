from django.db import models
from core.models.user_manager import UserManager
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# from rest_framework.authtoken.models import Token
# from django.conf import settings


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        help_text=_("Required. Letters, digits and @/./+/-/_ only."),
        validators=[EmailValidator()],
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    created_at = models.DateTimeField(auto_now=True, null=False, blank=False)
    modified_at = models.DateTimeField(auto_now=True, null=False, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["email"]
