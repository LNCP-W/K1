
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    AbstractUser,
)
from django.db import models, transaction


class UserModel(AbstractUser):
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "django_user"
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self):
        return self.username


class CurrencyModel(models.Model):
    name = models.CharField("Currency", max_length=255)

    class Meta:
        db_table = "django_app_currency"
        verbose_name = "currency"
        verbose_name_plural = "currencies"
        ordering = ["name"]

    def __str__(self):
        return self.name

class ProviderModel(models.Model):
    name = models.CharField("Provider", max_length=255)
    api_key = models.CharField("API Key", max_length=255, null=True, blank=True)
    link = models.CharField("Link", max_length=255)

    class Meta:
        db_table = "django_app_provider"
        verbose_name = "provider"
        verbose_name_plural = "providers"
        ordering = ["name"]

    def __str__(self):
        return self.name

class BlockModel(models.Model):
    fk_to_currency = models.ForeignKey(CurrencyModel, on_delete=models.CASCADE)
    number = models.IntegerField(null=False)
    created_at = models.DateTimeField(null=True)
    stored_at = models.DateTimeField(auto_now=True, null=False)
    provider = models.ForeignKey(ProviderModel, on_delete=models.CASCADE)

    class Meta:
        db_table = "django_app_block"
        verbose_name = "block"
        verbose_name_plural = "blocks"
        ordering = ["provider", "number"]
        indexes = [
            models.Index(fields=['number', 'provider']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['number', 'provider'], name='unique_block')
        ]

    def __str__(self):
        return f'{self.provider.name} {self.number}'

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(BlockModel, self).save(*args, **kwargs)

