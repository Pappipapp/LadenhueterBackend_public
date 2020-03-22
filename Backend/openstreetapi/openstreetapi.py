import hashlib
import sys

import overpy
from util import market_distance

api = overpy.Overpass()

days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
default_opening_hours = 'Mo-Fr 09:00-20:00'

english_day_abbreviations = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

dict_day_names = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def parse_opening_hours(opening_hours_string):
    """Parse opening hours string returned from openstreetmaps api

        Examples of possible strings
            Mo-Fr 09:00-13:00,15:00-18:30; Sa 09:00-13:30
            Mo-Sa 10:00-20:00; PH off

    """
    elements = opening_hours_string.split(';')       # Split by ';'
    elements = map(lambda x: x.strip(), elements)    # Strip whitespace left and right
    elements = map(lambda x: x.split(' '), elements) # Split by whitespace

    def maybe_translate(day_abbreviation):
        if day_abbreviation in english_day_abbreviations:
            return days[english_day_abbreviations.index(day_abbreviation)]

    def get_days_in_range(days_string):
        from_to_pairs = days_string.split(',')
        from_to_pairs = list(map(lambda x : x.split('-'), from_to_pairs))

        result = []
        for pair in from_to_pairs:
            if len(pair) == 1:
                result.append(pair[0])

            if len(pair) == 2:
                day_from = maybe_translate(pair[0])
                day_to   = maybe_translate(pair[1])

                result += (days[days.index(day_from) : days.index(day_to) + 1])

            #print('[ERROR] in parsing days string {}. Unkown amount of elements'.format(days_string))
            #return []

        return result

    opening_hours = {}

    for dict_day_name in dict_day_names:
        opening_hours[dict_day_name] = {'start': None, 'end': None}

    for element in elements:
        if len(element) > 1:
            days_string  = element[0]
            hours_string = element[1]

            hours_with_breaks = hours_string.split(',')

            from_to_pairs = []
            for hours in hours_with_breaks:
                from_to_pair = hours.split('-')
                from_to_pairs.append(from_to_pair)

            open_from = from_to_pairs[0][0]
            open_to = from_to_pairs[-1][-1]

            if open_from == 'off' or open_to == 'off':
                continue

            days_for_element = get_days_in_range(days_string)

            for day in days_for_element:
                if day in days:
                    opening_hours[dict_day_names[days.index(day)]]['start'] = open_from
                    opening_hours[dict_day_names[days.index(day)]]['end'] = open_to

    return opening_hours


def get_nearby_markets(lat1,lat2,lon1,lon2):

    def get_tag_value_or_none(node, element_name):
        """Check for given tag"""
        tag_value = node.tags.get(element_name, 'n/a')

        if 'n/a' == tag_value:
            return None

        return tag_value

    def try_get_latitude_longitude(entry):
        """Try to get lat lon info from node or way.

            - Try 'lat' 'lon' attributes of node
            - Try 'center_lat' 'center_lon' attributes of way
            - Try getting 'lat' and 'lon' attribute of first child node of way

        """
        latitude = None
        longitude = None

        if hasattr(entry, 'lat'):
            latitude = getattr(entry, 'lat')
        elif hasattr(entry, 'center_lat'):
            latitude = getattr(entry, 'center_lat')

        if hasattr(entry, 'lon'):
            longitude = getattr(entry, 'lon')
        elif hasattr(entry, 'center_lon'):
            longitude = getattr(entry, 'center_lon')

        if latitude is None or longitude is None:
            # Probably a way element without lat or lon attribute
            # Try getting the lat lon of the first node

            proxy_node = entry.get_nodes()[0]

            if hasattr(proxy_node, 'lat'):
                latitude = getattr(proxy_node, 'lat')

            if hasattr(proxy_node, 'lon'):
                longitude = getattr(proxy_node, 'lon')

        return latitude, longitude

    def get_nearby_markets_internal(lat1,lat2,lon1,lon2):
        # Queries all nodes and ways that have tag shop equal to supermarket around given bounding box
        query_string = """(node({0},{1},{2},{3})["shop"="supermarket"];
                            way({0},{1},{2},{3})["shop"="supermarket"];);
                           (._;>;);out body;""".format(lat1, lon1, lat2, lon2)

        result = api.query(query_string)

        # Combine node and way query results
        entries = result.nodes + result.ways
        markets = []
        for entry in entries:
            latitude, longitude = try_get_latitude_longitude(entry)

            if latitude is None or longitude is None:
                print('[ERROR] Node without latitude or longitude information')
                continue


            name          = get_tag_value_or_none(entry, 'name')
            street        = get_tag_value_or_none(entry, 'addr:street')
            housenumber   = get_tag_value_or_none(entry, 'addr:housenumber')
            postcode      = get_tag_value_or_none(entry, 'addr:postcode')
            city          = get_tag_value_or_none(entry, 'addr:city')
            opening_hours = get_tag_value_or_none(entry, 'opening_hours')

            # Do not accept entries without name information
            if name is None:
                continue

            # Entries without housenumber, postcode or city are accepted
            address_string = 'Keine Adresse gefunden'

            if street is not None:
                address_string = street
                if housenumber is not None:
                    address_string += ' ' + housenumber

                if postcode is not None:
                    address_string += ' ' + postcode

                if city is not None:
                    address_string += ' ' + city


            if opening_hours is None:
                opening_hours = default_opening_hours

            opening_hours_dict = parse_opening_hours(opening_hours)

            market_id = hashlib.sha256((str(latitude) + str(longitude)).encode('utf-8')).hexdigest()

            markets.append({
                'id': market_id,
                'name': name,
                'openingHours': opening_hours_dict,
                'address': address_string,
                'latitude': float(latitude),
                'longitude': float(longitude)
            })

        return markets

    markets = []
    iter = 0
    max_iter = 10
    min_markets = 15

    current_lat1 = lat1
    current_lat2 = lat2
    current_lon1 = lon1
    current_lon2 = lon2

    while len(markets) < min_markets and iter < max_iter:
        markets = get_nearby_markets_internal(current_lat1, current_lat2, current_lon1, current_lon2)
        print('[INFO] get_nearby_markets(...): Found {} markets in iteration {}'.format(len(markets), iter))

        # grow bounding box
        current_lat1 -= 0.05
        current_lat2 += 0.05
        current_lon1 -= 0.05
        current_lon2 += 0.05

        # try again
        iter += 1

    if len(list(markets)) == 0:
        raise ValueError
        return

    # Center of bounding box
    user_lat = lat1 + (lat2 - lat1) / 2
    user_lon = lon1 + (lon2 - lon1) / 2

    # Only get 25 closest markets
    for market in markets:
        dist = market_distance.calculate_distance_in_meters(user_lat, user_lon, market['latitude'], market['longitude'])
        market['dist_to_user'] = dist

    markets.sort(key=lambda market: market['dist_to_user'])

    print('[INFO] get_nearby_markets(...): Returning {} closest markets', len(markets) if len(markets) < 25 else 25)

    return markets[0:25]


if __name__ == '__main__':
    import json
    markets = get_nearby_markets(48.10, 48.15, 11.55, 11.59)
    print(json.dumps(markets))
