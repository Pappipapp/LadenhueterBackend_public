
# filter_by_distance

import math

def calculate_distance_in_meters(lat1_in_deg, lon1_in_deg, lat2_in_deg, lon2_in_deg):
    """
        "As the crow flies" distance between to points given as lat/lon

        Taken from <https://www.movable-type.co.uk/scripts/latlong.html>
    """
    def to_radians(degree):
        return (degree / 360.0) * 2.0 * math.pi

    earth_radius = 6371e3; # metres
    lat1  = to_radians(lat1_in_deg)
    lat2  = to_radians(lat2_in_deg)
    d_lat = to_radians(lat2_in_deg - lat1_in_deg)
    d_lon = to_radians(lon2_in_deg - lon1_in_deg)

    a = math.sin(d_lat / 2.0) * math.sin(d_lat / 2.0) + \
        math.cos(lat1) * math.cos(lat2) * \
        math.sin(d_lon / 2.0) * math.sin(d_lon / 2.0)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = earth_radius * c

    return d
