from django.contrib import admin

from . import models

EMPTY = "-пусто-"


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "url", "date", "parent", "size")
    readonly_fields = ("id",)
    empty_value_display = EMPTY
