from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound,HTTPFound
from pyramid.view import view_config
from pyramid.renderers import get_renderer

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Location,
    Service,
    ServiceDetail,
    Comment,
    TimingLoad,
    OperationDate
    )

def site_layout():
    renderer = get_renderer("templates/layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout

@view_config(route_name='home',renderer='templates/home.pt')
def home(request):
    return {"layout": site_layout(),
            "page_title": "Home"
            }

##### LOCATION ROUTES #####
@view_config(route_name='location_index',renderer='templates/location/index.pt')
def location_index(request):
    location_list = DBSession.query(Location).order_by(Location.name.asc()).all()
    return {"layout":site_layout(),
            "page_title":"Locations",
            "location_list":location_list}

@view_config(route_name='location_show',renderer='templates/location/show.pt')
def location_show(request):
    md = request.matchdict
    loc_id = md.get('id',None)
    if loc_id == None:
        loc_id = request.POST['id']
    location = DBSession.query(Location).filter_by(id=loc_id).first()
    return {"layout":site_layout(),
            "page_title": "Services for %s" % location.name,
            "location":location}

@view_config(route_name='location_new',renderer='templates/location/new.pt')
def location_new(request):
    return {"layout":site_layout(),
            "page_title": "Create a new location"}

@view_config(route_name='location_create',renderer='templates/error.pt')
def location_create(request):
    if 'form.submitted' in request.params:
        loc = Location(request.params['name'],request.params['postcode'],request.params['latitude'],request.params['longitude'])
        DBSession.add(loc)
        DBSession.flush()
        return HTTPFound(location = request.route_url('location_show',
                                                      id=loc.id))
    return {"layout":site_layout(),
           "page_title": "There has been an error",
           "error_message": request.params.keys()}

##### SERVICE ROUTES #####
@view_config(route_name='service_index',renderer='templates/service/index.pt')
def service_index(request):
    service_list = DBSession.query(Service).order_by(Service.signal_id.asc()).all()
    return {"layout":site_layout(),
            "page_title":"Services",
            "service_list":service_list}

@view_config(route_name='service_show',renderer='templates/service/show.pt')
def service_show(request):
    md = request.matchdict
    svc_id = md.get('id',None)
    if svc_id == None:
        svc_id = request.POST['id']
    service = DBSession.query(Service).filter_by(id=svc_id).first()
    return {"layout":site_layout(),
            "page_title": "Service Details for %s" % service.name,
            "service":service}

@view_config(route_name='service_new',renderer='templates/service/new.pt')
def service_new(request):
    timingload_list = DBSession.query(TimingLoad).order_by(TimingLoad.name.asc()).all()
    operation_date_list = DBSession.query(OperationDate).order_by(OperationDate.start_date.asc()).all()
    return {"layout":site_layout(),
            "timingload_list":timingload_list,
            "operation_date_list":operation_date_list,
            "page_title": "Create a new service"}

@view_config(route_name='service_create',renderer='templates/error.pt')
def service_create(request):
    if 'form.submitted' in request.params:
        svc = Service(request.params['signal_id'],request.params['operating_characteristics'],request.params['timing_load_id'],request.params['operatin_date_id'])
        DBSession.add(svc)
        DBSession.flush()
        return HTTPFound(service = request.route_url('service_show',
                                                      id=svc.id))
    return {"layout":site_layout(),
           "page_title": "There has been an error",
           "error_message": request.params.keys()}


##### TimingLoad ROUTES #####
@view_config(route_name='timingload_index',renderer='templates/timingload/index.pt')
def timingload_index(request):
    timingload_list = DBSession.query(TimingLoad).order_by(TimingLoad.name.asc()).all()
    return {"layout":site_layout(),
            "page_title":"TimingLoads",
            "timingload_list":timingload_list}

@view_config(route_name='timingload_show',renderer='templates/timingload/show.pt')
def timingload_show(request):
    md = request.matchdict
    tl_id = md.get('id',None)
    if tl_id == None:
        tl_id = request.POST['id']
    timingload = DBSession.query(TimingLoad).filter_by(id=tl_id).first()
    return {"layout":site_layout(),
            "page_title": "TimingLoad Details for %s" % timingload.name,
            "timingload":timingload}

@view_config(route_name='timingload_new',renderer='templates/timingload/new.pt')
def timingload_new(request):
    return {"layout":site_layout(),
            "page_title": "Create a new timingload"}

@view_config(route_name='timingload_create',renderer='templates/error.pt')
def timingload_create(request):
    if 'form.submitted' in request.params:
        tl = TimingLoad(request.params['name'],request.params['description'])
        DBSession.add(tl)
        DBSession.flush()
        return HTTPFound(location = request.route_url('timingload_show',
                                                      id=tl.id))
    return {"layout":site_layout(),
           "page_title": "There has been an error",
           "error_message": request.params.keys()}

