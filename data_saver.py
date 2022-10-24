from sqlalchemy import insert
from tables import device_table
from config import session
from geocode import reverse_geo_coder
import struct


"""------------------------------------------------- """
# import math

# def truncate(number, digits):
#     # 소수점 digits 자리 이후 값 버림
#     stepper = 10.0 ** digits
#     return math.trunc(stepper * number) / stepper

# lat = truncate(int(msg[10:18], 16)/1000000, 4)
# lon = truncate(int(msg[18: 26], 16)/1000000, 4)

# print("lat : ", lat)
# print("lat round plus : ", round(lat + 0.0002, 5))
# print("lat round minus : ", round(lat - 0.0002, 5))
# print('lon : ', lon)
# print("lon round plus : ", round(lon + 0.0002, 5))
# print('lon round minus : ', round(lon - 0.0002, 5))

# qs = Location.objects.filter(device__device_id=device_id, latitude__range=(
#     round(lat - 0.0002, 5), round(lat + 0.0002, 5)), longitude__range=(round(lon - 0.0002, 5), round(lon + 0.0002, 5)))

# location = qs.first() if len(qs) == 1 else min(qs, key=lambda x: abs(
#     x.latitude - lat and x.longitude - lon)) if len(qs) > 1 else None
"""------------------------------------------------- """


class InsertData:
    def __init__(self, device, location, oxygen, ph, conduct, chlorophyll):
        self.device = device
        self.location = location
        self.oxygen = oxygen
        self.ph = ph
        self.conduct = conduct
        self.chlorophyll = chlorophyll

    def device_insert(self, data):
        exist_id = session.query(device_table).filter(
            device_table.columns.device_id == int(data[:8], 16)).first()
        if exist_id is None:
            session.execute(insert(self.device).values(
                device_id=int(data[:8], 16),
                battery=int(data[8:10], 16)
            ))
            session.commit()
        else:
            pass

    def location_insert(self, data):
        lat = int(data[10:18], 16)/1000000
        lon = int(data[18:26], 16)/1000000

        reverse_geo = reverse_geo_coder(lat, lon)
        session.execute(insert(self.location).values(
            device_id=int(data[:8], 16),
            state=reverse_geo['state'],
            locality=reverse_geo['locality'],
            address=reverse_geo['address'],
            coordinate=[lat, lon],
            point='Point(%f %f)' % (lon, lat)
        ))
        session.commit()

    def oxygen_insert(self, data):
        session.execute(insert(self.oxygen).values(
            device_id=int(data[:8], 16),
            temperature=struct.unpack(
                '!f', bytes.fromhex(data[26:34]))[0],
            oxygen_per=struct.unpack(
                '!f', bytes.fromhex(data[34:42]))[0],
            oxygen_mpl=struct.unpack(
                '!f', bytes.fromhex(data[42:50]))[0],
            oxygen_ppm=struct.unpack(
                '!f', bytes.fromhex(data[50:58]))[0]
        ))
        session.commit()

    def ph_insert(self, data):
        session.execute(insert(self.ph).values(
            device_id=int(data[:8], 16),
            temperature=struct.unpack(
                '!f', bytes.fromhex(data[58:66]))[0],
            ph=struct.unpack('!f', bytes.fromhex(data[66:74]))[0],
            redox=struct.unpack(
                '!f', bytes.fromhex(data[74:82]))[0],
            ph_meter=struct.unpack(
                '!f', bytes.fromhex(data[82:90]))[0]
        ))
        session.commit()

    def conduct_insert(self, data):
        session.execute(insert(self.conduct).values(
            device_id=int(data[:8], 16),
            temperature=struct.unpack(
                '!f', bytes.fromhex(data[90:98]))[0],
            conductivity=struct.unpack(
                '!f', bytes.fromhex(data[98:106]))[0],
            salinity=struct.unpack(
                '!f', bytes.fromhex(data[106:114]))[0],
            tds=struct.unpack(
                '!f', bytes.fromhex(data[114:122]))[0]
        ))
        session.commit()

    def chlorophyll_insert(self, data):
        session.execute(insert(self.chlorophyll).values(
            device_id=int(data[:8], 16),
            temperature=int(data[130:134], 16) /
            (10 ** int(data[134:138], 16)),
            chlorophyll=int(data[122:126], 16) /
            (10 ** int(data[126:130], 16))
        ))
        session.commit()

    def __del__(self):
        session.close()
