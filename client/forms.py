from django import forms

from client.models import Client, Messages, Subscription


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('phone', 'FIO', 'comment', 'user',)


class ClientModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            "phone",
            "FIO",
            "comment",
            "user",
        )


class MessagesForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Messages
        fields = "__all__"


class MessagesModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Messages
        fields = (
            "topic",
            "text",
            "user",
        )


class SubscriptionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Subscription
        fields = "__all__"


class SubscriptionModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Subscription
        fields = (
            "created_at",
            "intervals",
            "status",
            "user",
        )
