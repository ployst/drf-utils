from django.contrib import admin

from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'label')

admin.site.register(Token, TokenAdmin)
