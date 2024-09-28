from django.contrib import admin

from client.models import Client, Subscription, Messages, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("FIO", "phone", "comment", "user")
    list_filter = ("FIO",)
    search_fields = ("FIO", "user")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("created_at", "intervals", "status", "user")
    list_filter = ("status",)
    search_fields = ("intervals", "status", "user")


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("topic", "text", "user")
    list_filter = ("topic",)
    search_fields = ("topic", "user")


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("last_attempt", "status_attempt", "report")
    list_filter = ("status_attempt",)
    search_fields = ("last_attempt", "status_attempt")
