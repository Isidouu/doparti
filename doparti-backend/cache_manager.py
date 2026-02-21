# cache_manager.py

from datetime import datetime, timedelta

# Diccionario en memoria
_CACHE = {}

# Tiempo de vida del cache (30 minutos)
_CACHE_DURATION = timedelta(minutes=30)


def get_from_cache(partido_id: int):
    """
    Devuelve el valor cacheado si existe y no expiró.
    Si expiró, lo elimina.
    """
    data = _CACHE.get(partido_id)

    if not data:
        return None

    if datetime.now() > data["expires"]:
        del _CACHE[partido_id]
        return None

    return data["value"]


def save_to_cache(partido_id: int, value: dict):
    """
    Guarda un valor en cache con tiempo de expiración.
    """
    _CACHE[partido_id] = {
        "value": value,
        "expires": datetime.now() + _CACHE_DURATION
    }