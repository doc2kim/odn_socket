from geopy.geocoders import Nominatim


def reverse_geo_coder(lat, lon):
    geo_locator = Nominatim(user_agent='odn')
    location = geo_locator.reverse(
        "%f, %f" % (lat, lon))
    results = location.raw.get('address')
    if 'province' in results and 'city' in results:
        state = "%s %s" % (results['province'], results['city'])
    elif 'province' in results:
        state = results['province']
    elif 'city' in results:
        state = results['city']
    else:
        state = None

    if 'county' in results or 'borough' in results:
        if 'county' in results:
            locality = results['county']
        else:
            locality = results['borough']
    else:
        locality = None

    if 'village' in results and 'town' in results:
        address = "%s, %s" % (results['town'], results['village'])
    elif 'village' in results:
        address = results['village']
    elif 'town' in results:
        address = results['town']
    else:
        address = None

    return {'state': state,
            'locality': locality,
            'address': address}
