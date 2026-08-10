import time

from django.core.cache import cache


def rate_limit(request, key_prefix, max_requests, window_seconds):
    """Simple rate limiter based on the client IP.

    Returns True if the request is allowed, False if it should be blocked.
    """
    ip = get_client_ip(request)
    cache_key = 'rl:{}:{}'.format(key_prefix, ip)
    now = int(time.time())

    attempts = cache.get(cache_key, [])
    attempts = [t for t in attempts if now - t < window_seconds]

    if len(attempts) >= max_requests:
        cache.set(cache_key, attempts, timeout=window_seconds)
        return False

    attempts.append(now)
    cache.set(cache_key, attempts, timeout=window_seconds)
    return True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    return ip
