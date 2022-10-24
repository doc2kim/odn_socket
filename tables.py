from sqlalchemy import Table, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from config import data_obj, engine
from geoalchemy2 import Geometry


device_table = Table("device_device",
                     data_obj,
                     Column('device_id', Integer, primary_key=True),
                     Column('device_type', String(50), default='buoy'),
                     Column('battery', Float),
                     Column('owner', String(200), default='ODN'),
                     Column('serial_number', String(50), default='SN-TRIPA-'),
                     Column('first_run_time', DateTime(
                         timezone=True), default=func.now()),
                     Column('operating_state', Boolean, default=True),
                     autoload_with=engine)

location_table = Table("device_location",
                       data_obj,
                       Column('measured_time', DateTime(
                           timezone=True), default=func.now()),
                       Column('point', Geometry('POINT')),
                       autoload_with=engine)

oxygen_table = Table("device_oxygen",
                     data_obj,
                     Column('measured_time', DateTime(
                         timezone=True), default=func.now()),
                     Column('serial_number', String(50), default='SN-PODOC-'),
                     autoload_with=engine)

ph_table = Table("device_ph", data_obj,
                 Column('measured_time', DateTime(
                     timezone=True), default=func.now()),
                 Column('serial_number', String(50), default='SN-PPHRB-'),
                 autoload_with=engine)

conduct_table = Table("device_conduct",
                      data_obj,
                      Column('measured_time', DateTime(
                          timezone=True), default=func.now()),
                      Column('serial_number', String(50), default='SN-PC4EB-'),
                      autoload_with=engine)

chlorophyll_table = Table("device_chlorophyll",
                          data_obj,
                          Column('measured_time', DateTime(
                              timezone=True), default=func.now()),
                          Column('serial_number', String(50), default='SN-'),
                          autoload_with=engine)
