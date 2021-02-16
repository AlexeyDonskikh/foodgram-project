from django.contrib import admin

from api.models import Favorite, Purchase, Subscription


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')
    autocomplete_fields = ('user', 'author')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')
