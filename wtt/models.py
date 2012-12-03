from sqlalchemy import (
    Time,
    Boolean,
    Unicode,
    Column,
    Integer,
    String,
    DateTime,
    Date,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer(length=10), primary_key=True)
    name = Column(String(length=255), unique=True)
    postcode = Column(String(length=255))
    latitude = Column(String(length=255))
    longitude = Column(String(length=255))

    def __init__(self, name, postcode = None, latitude = None, longitude = None):
        self.name = name
        self.postcode = postcode
        self.latitude = latitude
        self.longitude = longitude

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer(length=10), primary_key=True)
    author = Column(Unicode(length=100))
    created = Column(DateTime)
    remote_ip = Column(Unicode(25))
    content = Column(String(length=255))

    def __init__(self,author,created,remote_ip,content):
        self.author = author
        self.created = created
        self.remote_ip = remote_ip
        self.content = content

class OperationDate(Base):
    __tablename__ = 'operation_dates'
    id = Column(Integer(length=10), primary_key=True)
    start_date = Column(Date)
    end_date   = Column(Date)

    def __init__(self,start_date,end_date):
        self.start_date = start_date
        self.end_date = end_date


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer(length=10), primary_key=True)
    signal_id = Column(Unicode(20))
    operating_characteristics = Column(String(length=255))
    timing_load_id = Column(Integer(length=10),ForeignKey('timingloads.id'))
    operation_date_id = Column(Integer(length=10),ForeignKey('operation_dates.id'))

    def __init__(self,signal_id,operating_characteristics=None,timing_load_id=None, operation_date_id = None):
        self.signal_id = signal_id
        self.operating_characteristics = operating_characteristics
        self.timing_load_id = timing_load_id
        self.operation_date_id = operation_date_id

class TimingLoad(Base):
    __tablename__ = 'timingloads'
    id = Column(Integer(length=10), primary_key=True)
    name = Column(Unicode(length=100))
    description = Column(String(length=255))

    def __init__(self, name, description):
        self.name = name
        self.description = description

class ServiceDetail(Base):
    __tablename__ = "servicedetails"
    id = Column(Integer(length=10), primary_key=True)
    location_id = Column(Integer(length=10),ForeignKey('locations.id'))
    service_id = Column(Integer(length=10),ForeignKey('services.id'))
    is_origin = Column(Boolean)
    is_destination = Column(Boolean)
    time_in = Column(Time)
    time_out = Column(Time)

    def __init__(self,location_id,service_id,is_origin,is_destination,time_in,time_out):
        self.location_id = location_id
        self.service_id = service_id
        self.is_origin = is_origin
        self.is_destination = is_destination
        self.time_in = time_id
        self.time_out = time_out

class LocationComment(Base):
    __tablename__ = "locationcomments"
    id = Column(Integer(length=10), primary_key=True)
    location_id = Column(Integer(length=10),ForeignKey('locations.id'))
    comment_id = Column(Integer(length=10),ForeignKey('comments.id'))

    def __init__(self,location_id,comment_id):
        self.location_id = location_id
        self.comment_id = comment_id

class ServiceComment(Base):
    __tablename__ = "servicecomments"
    id = Column(Integer(length=10), primary_key=True)
    service_id = Column(Integer(length=10),ForeignKey('services.id'))
    comment_id = Column(Integer(length=10),ForeignKey('comments.id'))

    def __init__(self,services_id,comment_id):
        self.services_id = services_id
        self.comment_id = comment_id


