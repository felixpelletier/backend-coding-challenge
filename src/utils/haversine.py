
import math

EARTHS_RADIUS_KM = 6371.0


def compute_harvesine_distance(location1, location2):
    """
        References:
             - https://en.wikipedia.org/wiki/Haversine_formula
             - https://en.wikipedia.org/wiki/Earth_radius#Mean_radius
    """

    latitude1_rad, longitude1_rad = coordinates_deg2rad(location1)
    latitude2_rad, longitude2_rad = coordinates_deg2rad(location2)

    delta_latitude = latitude1_rad - latitude2_rad
    delta_longitude = longitude1_rad - longitude2_rad

    # h = haversine of central angle
    h = haversine(delta_latitude) \
        + math.cos(latitude2_rad) * math.cos(latitude1_rad) * haversine(delta_longitude)

    distance = 2.0 * EARTHS_RADIUS_KM * math.asin(math.sqrt(h))

    return distance


def haversine(angle):
    return (1.0 - math.cos(angle)) / 2.0


def coordinates_deg2rad(location):
    latitude_deg, longitude_deg = location
    latitude_rad = math.radians(latitude_deg)
    longitude_rad = math.radians(longitude_deg)
    return latitude_rad, longitude_rad
