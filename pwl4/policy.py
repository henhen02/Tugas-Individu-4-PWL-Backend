from pyramid.csrf import CookieCSRFStoragePolicy


class SecurityPolicy:
    def __init__(self, secret):
        self.secret = secret

    def load_credentials(self, request):  # Load credentials from request headers
        token = request.headers.get("X-Auth-Token")
        if token:
            return {"token": token}
        return None

    def identify(self, request):
        return None

    def remember(self, request, userid, **kw):
        return []

    def forget(self, request):
        return []


def includeme(config):
    config.set_csrf_storage_policy(CookieCSRFStoragePolicy())
    config.set_default_csrf_options(require_csrf=True)
