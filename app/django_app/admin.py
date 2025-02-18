from django.contrib import admin

from .models import UserModel, ProviderModel, CurrencyModel

admin.site.register(UserModel)
admin.site.register(ProviderModel)
admin.site.register(CurrencyModel)

