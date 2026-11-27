from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с API сервисов."""

    @abstractmethod
    def _connect(self, url: str, params: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
        """Приватный метод подключения к API и проверки статус-кода."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> List[List[Any]]:
        """Получение данных о самолетах в воздушном пространстве страны."""
        pass


class AeroplanesAPI(BaseAPI):
    """Класс для получения координат страны и данных о самолетах."""

    def __init__(self) -> None:
        self.__nominatim_url = "https://nominatim." + "openstreetmap.org" + "/search"
        self.__opensky_url = "https://opensky-network.org" + "/api/states/all"
        self.__headers = {"User-Agent": "FlightTrackerCoursework/1.0"}

    def _connect(self, url: str, params: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Any:
        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при обращении к API ({url}): {e}")
            return None

    def __get_country_bbox(self, country: str) -> Optional[List[str]]:
        """Получает boundingbox [south, north, west, east] для заданной страны."""
        params = {
            "q": country,
            "format": "json",
            "limit": 1
        }
        data = self._connect(self.__nominatim_url, params=params, headers=self.__headers)
        if data and isinstance(data, list) and len(data) > 0 and "boundingbox" in data[0]:
            return data[0]["boundingbox"]
        return None

    def get_aeroplanes(self, country: str) -> List[List[Any]]:
        bbox = self.__get_country_bbox(country)
        if not bbox or len(bbox) < 4:
            print(f"Не удалось определить границы для страны: {country}")
            return []

        params = {
            "lamin": bbox[0],  # южная граница
            "lamax": bbox[1],  # северная граница
            "lomin": bbox[2],  # западная граница
            "lomax": bbox[3],  # восточная граница
        }
        data = self._connect(self.__opensky_url, params=params)
        if data and isinstance(data, dict) and data.get("states"):
            return data["states"]
        return []
