from random import sample

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.cache import cache

from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.services import get_blogs_from_cache
from client.forms import SubscriptionForm, SubscriptionModeratorForm, ClientForm, ClientModeratorForm, MessagesForm, \
    MessagesModeratorForm
from client.models import Client, Subscription, Messages, Mailing
from client.services import get_client_from_cache


@login_required
def base(request):
    # Получение данных из кэша или базы данных
    total_mailings = cache.get("total_mailings")
    if total_mailings is None:
        total_mailings = Mailing.objects.count()
        cache.set("total_mailings", total_mailings)

    active_mailings = cache.get("is_active_mailings")
    if active_mailings is None:
        active_mailings = Mailing.objects.filter(is_active=True).count()
        cache.set("active_mailings", active_mailings)

    unique_clients = cache.get("unique_clients")
    if unique_clients is None:
        unique_clients = Client.objects.count()
        cache.set("unique_clients", unique_clients)

    random_blogs = cache.get("random_blogs")
    if random_blogs is None:
        blogs = list(get_blogs_from_cache())  # Преобразуем QuerySet в список
        if len(blogs) > 3:
            random_blogs = sample(blogs, 3)  # Выбираем 3 случайных блога
        else:
            random_blogs = blogs  # Если меньше 3 блогов, выбираем все
        cache.set("random_blogs", random_blogs)

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
        "random_blogs": random_blogs,
    }

    return render(request, "client/base.html", context)
"""вьюшки для модели Клиента"""


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/client_list.html"

    def get_queryset(self):
        return get_client_from_cache()


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "client/client_detail.html"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client:client_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("client:client_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ClientFormset = inlineformset_factory(Client, Messages, Subscription, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = ClientFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = ClientFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return ClientModeratorForm
        if (
                user.has_perm("client.can_cancel_publication")
                and user.has_perm("client.can_change_description")
                and user.has_perm("client.can_change_product_category")
        ):
            return ClientForm


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy("client:client_list")


"""вьюшки для модели Рассылки"""


class SubscriptionListView(LoginRequiredMixin, ListView):
    model = Subscription
    template_name = "client/subscription_list.html"

    def get_queryset(self):
        return get_client_from_cache()


class SubscriptionDetailView(LoginRequiredMixin, DetailView):
    model = Subscription
    template_name = "client/subscription_detail.html"


class SubscriptionCreateView(LoginRequiredMixin, CreateView):
    model = Subscription
    form_class = SubscriptionForm
    success_url = reverse_lazy("client:subscription_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SubscriptionUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscription
    form_class = SubscriptionForm
    success_url = reverse_lazy("client:subscription_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubscriptionFormset = inlineformset_factory(Client, Messages, Subscription, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = SubscriptionFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = SubscriptionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return SubscriptionModeratorForm
        if (
                user.has_perm("client.can_cancel_publication")
                and user.has_perm("client.can_change_description")
                and user.has_perm("client.can_change_product_category")
        ):
            return SubscriptionForm


class SubscriptionDeleteView(LoginRequiredMixin, DeleteView):
    model = Subscription
    success_url = reverse_lazy("client:subscription_list")


"""вьюшки для модели Сообщений"""


class MessagesListView(LoginRequiredMixin, ListView):
    model = Messages
    template_name = "client/messages_list.html"

    def get_queryset(self):
        return get_client_from_cache()


class MessagesDetailView(LoginRequiredMixin, DetailView):
    model = Messages
    template_name = "client/messages_detail.html"


class MessagesCreateView(LoginRequiredMixin, CreateView):
    model = Messages
    form_class = MessagesForm
    success_url = reverse_lazy("client:messages_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessagesUpdateView(LoginRequiredMixin, UpdateView):
    model = Messages
    form_class = MessagesForm
    success_url = reverse_lazy("client:messages_list")

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MessagesFormset = inlineformset_factory(Client, Messages, Subscription, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = MessagesFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = MessagesFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return MessagesModeratorForm
        if (
                user.has_perm("client.can_cancel_publication")
                and user.has_perm("client.can_change_description")
                and user.has_perm("client.can_change_product_category")
        ):
            return MessagesForm


class MessagesDeleteView(LoginRequiredMixin, DeleteView):
    model = Messages
    success_url = reverse_lazy("client:messages_list")
