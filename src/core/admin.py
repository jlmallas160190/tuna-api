from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Menu, Translation


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ("key", "language", "text")
    search_fields = ("key", "text")
    list_filter = ("language",)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("key", "icon", "url")
    search_fields = ("key", "url")
    list_filter = ("is_active",)
    fieldsets = (
        (None, {"fields": ("key", "icon", "url", "parent", "groups", "is_active")}),
    )
    verbose_name = _("Menu")
    verbose_name_plural = _("Menus")
