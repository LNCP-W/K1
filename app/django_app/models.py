from django.db import models


class User(models.Model):
    username = models.CharField('Username', max_length=120)
    email = models.EmailField("email address",max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]
