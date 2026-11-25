from typing import List
from src.aeroplane import Aeroplane


def filter_aeroplanes(aeroplanes: List[Aeroplane], filter_words: str) -> List[Aeroplane]:
    """Фильтрует самолеты по странам регистрации (через пробел или запятую)."""
    if not filter_words.strip():
        return aeroplanes
    countries = [word.strip().lower() for word in filter_words.replace(",", " ").split() if word.strip()]
    return [
        plane for plane in aeroplanes
        if any(country in plane.origin_country.lower() for country in countries)
    ]


def get_aeroplanes_by_altitude(aeroplanes: List[Aeroplane], altitude_range: str) -> List[Aeroplane]:
    """Фильтрует самолеты по диапазону высот (формат: '1000 - 10000')."""
    if not altitude_range.strip():
        return aeroplanes
    try:
        parts = altitude_range.replace(" ", "").split("-")
        if len(parts) != 2:
            raise ValueError
        min_alt, max_alt = float(parts[0]), float(parts[1])
        if min_alt > max_alt:
            min_alt, max_alt = max_alt, min_alt
        return [plane for plane in aeroplanes if min_alt <= plane.altitude <= max_alt]
    except ValueError:
        print("Некорректный формат диапазона высот. Фильтр по высоте пропущен.")
        return aeroplanes


def sort_aeroplanes(aeroplanes: List[Aeroplane]) -> List[Aeroplane]:
    """Сортирует самолеты по убыванию высоты (DESC)."""
    return sorted(aeroplanes, reverse=True)


def get_top_aeroplanes(aeroplanes: List[Aeroplane], top_n: int) -> List[Aeroplane]:
    """Возвращает топ N самолетов."""
    if top_n <= 0:
        return []
    return aeroplanes[:top_n]


def print_aeroplanes(aeroplanes: List[Aeroplane]) -> None:
    """Выводит список самолетов в человекочитаемом виде."""
    if not aeroplanes:
        print("Самолеты по заданным критериям не найдены.")
        return
    print(f"\nНайдено самолетов: {len(aeroplanes)}")
    print("-" * 85)
    for plane in aeroplanes:
        print(plane)
    print("-" * 85)
