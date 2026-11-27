import pytest
from src.aeroplane import Aeroplane
from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes,
)


@pytest.fixture
def sample_planes():
    return [
        Aeroplane("P1", "Spain", 200.0, 5000.0),
        Aeroplane("P2", "Germany", 250.0, 11000.0),
        Aeroplane("P3", "United States", 230.0, 8000.0),
    ]


def test_filter_aeroplanes(sample_planes):
    filtered = filter_aeroplanes(sample_planes, "Spain, Germany")
    assert len(filtered) == 2
    assert filter_aeroplanes(sample_planes, "") == sample_planes


def test_get_aeroplanes_by_altitude(sample_planes):
    ranged = get_aeroplanes_by_altitude(sample_planes, "6000 - 12000")
    assert len(ranged) == 2
    assert ranged[0].callsign == "P2"

    # Проверка некорректного формата (должен вернуть исходный список без падения)
    invalid = get_aeroplanes_by_altitude(sample_planes, "invalid_range")
    assert len(invalid) == 3


def test_sort_and_top_aeroplanes(sample_planes):
    sorted_planes = sort_aeroplanes(sample_planes)
    assert [p.callsign for p in sorted_planes] == ["P2", "P3", "P1"]

    top_2 = get_top_aeroplanes(sorted_planes, 2)
    assert len(top_2) == 2
    assert top_2[0].callsign == "P2"
    assert get_top_aeroplanes(sorted_planes, 0) == []


def test_print_aeroplanes(sample_planes, capsys):
    print_aeroplanes(sample_planes)
    captured = capsys.readouterr()
    assert "Найдено самолетов: 3" in captured.out

    print_aeroplanes([])
    captured_empty = capsys.readouterr()
    assert "не найдены" in captured_empty.out
