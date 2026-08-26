from django.core.cache import cache
from rest_framework.throttling import SimpleRateThrottle


class FixedWindowThrottle(SimpleRateThrottle):

    def get_cache_key(self, request, view):
        # Client ka IP address
        ip = self.get_ident(request)

        # Har throttle ka separate cache key
        return f"throttle:{self.scope}:{ip}"

    def allow_request(self, request, view):

        # Cache key
        self.key = self.get_cache_key(request, view)

        # Cache se previous data nikalo
        self.history = cache.get(self.key)

        # --------------------------------
        # FIRST REQUEST
        # --------------------------------

        if self.history is None:

            self.history = {
                'count': 1,
                'start': self.timer()
            }

            cache.set(
                self.key,
                self.history,
                self.duration
            )

            return True

        # --------------------------------
        # CHECK TIME
        # --------------------------------

        elapsed = self.timer() - self.history['start']

        # Agar complete 1 minute ho gaya
        if elapsed >= self.duration:

            self.history = {
                'count': 1,
                'start': self.timer()
            }

            cache.set(
                self.key,
                self.history,
                self.duration
            )

            return True

        # --------------------------------
        # REQUEST IS WITHIN LIMIT
        # --------------------------------

        if self.history['count'] < self.num_requests:

            self.history['count'] += 1

            cache.set(
                self.key,
                self.history,
                self.duration
            )

            return True

        # --------------------------------
        # THROTTLED
        # --------------------------------

        # IMPORTANT:
        # Yahan start time CHANGE NAHI karna hai.
        #
        # Jo time first throttling par set hua tha,
        # wahi timer rahega.

        return False

    def wait(self):

        if not self.history:
            return None

        # First throttling/start time se elapsed time
        elapsed = self.timer() - self.history['start']

        # Kitna time remaining hai
        remaining = self.duration - elapsed

        return max(remaining, 0)


# =====================================
# LOGIN
# =====================================

class LoginThrottle(FixedWindowThrottle):
    scope = 'login'


# =====================================
# BLOG CREATE
# =====================================

class BlogCreateThrottle(FixedWindowThrottle):
    scope = 'blog_create'


# =====================================
# BLOG SHOW
# =====================================

class BlogShowThrottle(FixedWindowThrottle):
    scope = 'blog_show'


# =====================================
# REGISTRATION
# =====================================

class RegistrationThrottle(FixedWindowThrottle):
    scope = 'registration'


# =====================================
# REFRESH TOKEN
# =====================================

class RefreshTokenThrottle(FixedWindowThrottle):
    scope = 'refresh_token'