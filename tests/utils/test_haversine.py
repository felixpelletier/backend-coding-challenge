from src.utils import haversine

RELATIVE_TOLERANCE = 0.01


def assert_correct_distance(expected, actual):
    absolute_tolerance = RELATIVE_TOLERANCE * expected
    absolute_error = abs(expected - actual)
    assert absolute_error < absolute_tolerance


def test_compute_haversine_distance_north_east():
    expected_distance = 6830.0
    quebec = (46.816667, -71.216667)
    moscow = (55.75, 37.616667)
    actual_distance = haversine.compute_harvesine_distance(quebec, moscow)
    assert_correct_distance(expected_distance, actual_distance)


def test_compute_haversine_distance_north_west():
    expected_distance = 3188.2
    quebec = (46.816667, -71.216667)
    yellowknife = (62.442222, -114.3975)
    actual_distance = haversine.compute_harvesine_distance(quebec, yellowknife)
    assert_correct_distance(expected_distance, actual_distance)


def test_compute_haversine_distance_south_east():
    expected_distance = 16907.3
    quebec = (46.816667, -71.216667)
    melbourne = (-37.813611, 144.963056)
    actual_distance = haversine.compute_harvesine_distance(quebec, melbourne)
    assert_correct_distance(expected_distance, actual_distance)


def test_compute_haversine_distance_south_west():
    expected_distance = 4250.1
    quebec = (46.816667, -71.216667)
    san_francisco = (37.783333, -122.416667)
    actual_distance = haversine.compute_harvesine_distance(quebec, san_francisco)
    assert_correct_distance(expected_distance, actual_distance)
