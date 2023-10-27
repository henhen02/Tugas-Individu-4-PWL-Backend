from pyramid.config import Configurator
from pyramid.security import ALL_PERMISSIONS
from pyramid.authorization import ACLAuthorizationPolicy, Allow

from .middleware import access_control


class RootAccess(object):
    __access__ = [(Allow, "admin", ALL_PERMISSIONS), (Allow, "user")]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """This function returns a Pyramid WSGI application."""
    with Configurator(settings=settings) as config:
        config.include("pyramid_chameleon")
        config.set_root_factory(RootAccess)
        config.set_authorization_policy(ACLAuthorizationPolicy())
        config.include("pyramid_jwt")
        config.set_jwt_authentication_policy(
            "secret",
            expiration=3600,
            auth_type="Bearer",
            callback=access_control.add_rules,
        )
        config.include(".routes")
        config.include(".models")
        config.scan()
    return config.make_wsgi_app()
