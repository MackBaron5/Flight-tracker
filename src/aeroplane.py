from typing import Any, Dict, List, Optional


class Aeroplane:
    """Класс для представления информации о самолете."""

    __slots__ = ("__callsign", "__origin_country", "__velocity", "__altitude")

    def __init__(
        self,
        callsign: Optional[str],
        origin_country: Optional[str],
        velocity: Optional[float],
        altitude: Optional[float]
    ) -> None:
        self.__callsign = self.__validate_str(callsign, "Неизвестен")
        self.__origin_country = self.__validate_str(origin_country, "Неизвестна")
        self.__velocity = self.__validate_float(velocity)
        self.__altitude = self.__validate_float(altitude)

    @staticmethod
    def __validate_str(value: Optional[str], default: str) -> str:
        if isinstance(value, str) and value.strip():
            return value.strip()
        return default

    @staticmethod
    def __validate_float(value: Optional[float]) -> float:
        if isinstance(value, (int, float)) and value >= 0:
            return float(value)
        return 0.0

    @property
    def callsign(self) -> str:
        return self.__callsign

    @property
    def origin_country(self) -> str:
        return self.__origin_country

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def altitude(self) -> float:
        return self.__altitude

    # Методы сравнения (по высоте полета, при равной высоте — по скорости)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__altitude, self.__velocity) == (other.__altitude, other.__velocity)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__altitude, self.__velocity) < (other.__altitude, other.__velocity)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__altitude, self.__velocity) <= (other.__altitude, other.__velocity)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__altitude, self.__velocity) > (other.__altitude, other.__velocity)

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.__altitude, self.__velocity) >= (other.__altitude, other.__velocity)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект в словарь для сохранения в JSON."""
        return {
            "callsign": self.__callsign,
            "origin_country": self.__origin_country,
            "velocity": self.__velocity,
            "altitude": self.__altitude,
        }

    @classmethod
    def cast_to_object_list(cls, raw_data: List[List[Any]]) -> List["Aeroplane"]:
        """Преобразует сырой список списков от OpenSky API в список объектов Aeroplane."""
        aeroplanes = []
        for item in raw_data:
            if len(item) >= 14:
                altitude = item[7] if item[7] is not None else item[13]
                plane = cls(
                    callsign=item[1],
                    origin_country=item[2],
                    velocity=item[9],
                    altitude=altitude
                )
                aeroplanes.append(plane)
        return aeroplanes

    def __str__(self) -> str:
        return (
            f"Рейс: {self.__callsign:<10} | Страна: {self.__origin_country:<18} | "
            f"Высота: {self.__altitude:>8.1f} м | Скорость: {self.__velocity:>6.1f} м/с"
        )
