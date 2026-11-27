from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.storage import JSONSaver
from src.utils import (
    filter_aeroplanes,
    get_aeroplanes_by_altitude,
    get_top_aeroplanes,
    print_aeroplanes,
    sort_aeroplanes,
)


def user_interaction() -> None:
    api = AeroplanesAPI()
    json_saver = JSONSaver()

    country = input("Введите название страны для поиска самолетов (например, Spain или Russia): ").strip()
    if not country:
        print("Название страны не может быть пустым.")
        return

    print("Загружаем данные с серверов...")
    raw_aeroplanes = api.get_aeroplanes(country)
    if not raw_aeroplanes:
        print("Данные о самолетах не получены.")
        return

    aeroplanes = Aeroplane.cast_to_object_list(raw_aeroplanes)

    # Сохраняем полученные самолеты в JSON-файл
    for plane in aeroplanes:
        json_saver.add_aeroplane(plane)

    try:
        top_n_input = input("Введите количество самолетов для вывода в топ N (по умолчанию 10): ").strip()
        top_n = int(top_n_input) if top_n_input else 10
    except ValueError:
        print("Введено не число. Будет использовано значение по умолчанию: 10.")
        top_n = 10

    filter_words = input("Введите названия стран для фильтрации по стране регистрации (или Enter для пропуска): ")
    altitude_range = input("Введите диапазон высот полета в метрах (например: 5000 - 12000, или Enter): ")

    filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)
    ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)
    sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)

    print_aeroplanes(top_aeroplanes)


if __name__ == "__main__":
    user_interaction()
