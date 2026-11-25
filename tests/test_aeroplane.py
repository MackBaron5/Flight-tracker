from src.aeroplane import Aeroplane


def test_aeroplane_init_valid():
    plane = Aeroplane("  UAL1621  ", "United States", 250.5, 10000.0)
    assert plane.callsign == "UAL1621"
    assert plane.origin_country == "United States"
    assert plane.velocity == 250.5
    assert plane.altitude == 10000.0


def test_aeroplane_init_invalid_values():
    plane = Aeroplane(None, "", -50.0, None)
    assert plane.callsign == "Неизвестен"
    assert plane.origin_country == "Неизвестна"
    assert plane.velocity == 0.0
    assert plane.altitude == 0.0


def test_aeroplane_comparisons():
    plane_low = Aeroplane("AAA111", "Spain", 200.0, 5000.0)
    plane_high = Aeroplane("BBB222", "France", 220.0, 10000.0)
    plane_same_alt_faster = Aeroplane("CCC333", "Germany", 260.0, 10000.0)

    assert plane_low < plane_high
    assert plane_low <= plane_high
    assert plane_high > plane_low
    assert plane_high >= plane_low
    assert plane_high != plane_low
    assert plane_high < plane_same_alt_faster
    assert plane_high == Aeroplane("DDD444", "Italy", 220.0, 10000.0)


def test_aeroplane_to_dict_and_str():
    plane = Aeroplane("AFL123", "Russia", 230.0, 9500.0)
    assert plane.to_dict() == {
        "callsign": "AFL123",
        "origin_country": "Russia",
        "velocity": 230.0,
        "altitude": 9500.0,
    }
    assert "AFL123" in str(plane)
    assert "Russia" in str(plane)


def test_cast_to_object_list():
    raw_data = [
        [
            "4b1812", "SWR123 ", "Switzerland", 1600000, 1600000,
            8.5, 47.4, 8000.0, False, 210.0, 90.0, 0.0, None, 8100.0
        ],
        ["short_invalid_list"]
    ]
    planes = Aeroplane.cast_to_object_list(raw_data)
    assert len(planes) == 1
    assert planes[0].callsign == "SWR123"
    assert planes[0].altitude == 8000.0
