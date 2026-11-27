import pytest
from src.aeroplane import Aeroplane
from src.storage import JSONSaver


@pytest.fixture
def temp_saver(tmp_path):
    file_path = tmp_path / "test_planes.json"
    return JSONSaver(str(file_path))


def test_json_saver_add_and_get(temp_saver):
    plane1 = Aeroplane("TEST1", "Spain", 200.0, 8000.0)
    plane2 = Aeroplane("TEST2", "France", 240.0, 11000.0)

    temp_saver.add_aeroplane(plane1)
    temp_saver.add_aeroplane(plane2)
    # Повторное добавление дубликата не должно создавать вторую запись
    temp_saver.add_aeroplane(plane1)

    all_planes = temp_saver.get_aeroplanes({})
    assert len(all_planes) == 2

    spain_planes = temp_saver.get_aeroplanes({"origin_country": "Spain"})
    assert len(spain_planes) == 1
    assert spain_planes[0]["callsign"] == "TEST1"


def test_json_saver_delete(temp_saver):
    plane1 = Aeroplane("TEST1", "Spain", 200.0, 8000.0)
    plane2 = Aeroplane("TEST2", "France", 240.0, 11000.0)

    temp_saver.add_aeroplane(plane1)
    temp_saver.add_aeroplane(plane2)
    temp_saver.delete_aeroplane(plane1)

    remaining = temp_saver.get_aeroplanes({})
    assert len(remaining) == 1
    assert remaining[0]["callsign"] == "TEST2"
