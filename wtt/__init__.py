from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    Location,
    Service,
    TimingLoad,
    OperationDate
)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('location_index', '/location')
    config.add_route('location_new', '/location/new')
    config.add_route('location_create', '/location/create')
    config.add_route('location_show', '/location/{id}')
    config.add_route('timingload_index', '/timingload')
    config.add_route('timingload_new',   '/timingload/new')
    config.add_route('timingload_create','/timingload/create')
    config.add_route('timingload_show',  '/timingload/{id}')
    config.add_route('service_index', '/service')
    config.add_route('service_new',   '/service/new')
    config.add_route('service_create','/service/create')
    config.add_route('service_show',  '/service/{id}')
    config.scan()
    return config.make_wsgi_app()

