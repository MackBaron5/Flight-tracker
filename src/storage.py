from abc import ABC, abstractmethod
import json
import os
from typing import Any, Dict, List
from src.aeroplane import Aeroplane


class BaseStorage(ABC):
    """Абстрактный класс для работы с хранилищем данных."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        pass

    @abstractmethod
    def get_aeroplanes(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        pass


class JSONSaver(BaseStorage):
    """Класс для сохранения информации о самолетах в JSON-файл."""

    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        self.__filename = filename
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)

    def _read_file(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.__filename):
            return []
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                content = json.load(file)
                return content if isinstance(content, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_file()
        plane_dict = aeroplane.to_dict()
        # Избегаем дублирования записей с одинаковым позывным и страной
        if not any(
            item.get("callsign") == plane_dict["callsign"]
            and item.get("origin_country") == plane_dict["origin_country"]
            for item in data
        ):
            data.append(plane_dict)
            self._write_file(data)

    def get_aeroplanes(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        data = self._read_file()
        if not criteria:
            return data
        result = []
        for item in data:
            if all(item.get(k) == v for k, v in criteria.items()):
                result.append(item)
        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._read_file()
        updated_data = [
            item for item in data
            if not (
                    item.get("callsign") == aeroplane.callsign
                    and item.get("origin_country") == aeroplane.origin_country
            )
        ]
        self._write_file(updated_data)
