from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig

from client.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    SubscriptionListView, SubscriptionDetailView, SubscriptionCreateView, SubscriptionUpdateView, \
    SubscriptionDeleteView, MessagesListView, MessagesDetailView, MessagesCreateView, MessagesUpdateView, \
    MessagesDeleteView, base

app_name = ClientConfig.name

urlpatterns = [
    path("", base, name="base"),
    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name="client_create"),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name="client_update"),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name="client_delete"),
    path('subscription/', cache_page(60)(SubscriptionListView.as_view()), name='subscription_list'),
    path('subscription/<int:pk>/', SubscriptionDetailView.as_view(), name='subscription_detail'),
    path('subscription/create/', SubscriptionCreateView.as_view(), name="subscription_create"),
    path('subscription/<int:pk>/update/', SubscriptionUpdateView.as_view(), name="subscription_update"),
    path('subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name="subscription_delete"),
    path('messages/', cache_page(60) (MessagesListView.as_view()), name='messages_list'),
    path('messages/<int:pk>/', MessagesDetailView.as_view(), name='messages_detail'),
    path('messages/create/', MessagesCreateView.as_view(), name="messages_create"),
    path('messages/<int:pk>/update/', MessagesUpdateView.as_view(), name="messages_update"),
    path('messages/<int:pk>/delete/', MessagesDeleteView.as_view(), name="messages_delete"),
]
