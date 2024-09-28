from django.core.cache import cache

from client.models import Client
from config.settings import CACHE_ENABLED


def get_client_from_cache():
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = "client_list"
    client = cache.get(key)
    if client is not None:
        return client
    client = Client.objects.all()
    cache.set(key, client)
    return client# Cache for 1 hour