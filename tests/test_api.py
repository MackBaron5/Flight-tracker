from unittest.mock import MagicMock, patch
import requests
from src.api import AeroplanesAPI


@patch("src.api.requests.get")
def test_get_aeroplanes_success(mock_get):
    mock_nominatim = MagicMock()
    mock_nominatim.status_code = 200
    mock_nominatim.json.return_value = [{"boundingbox": ["36.0", "43.8", "-9.3", "3.3"]}]

    mock_opensky = MagicMock()
    mock_opensky.status_code = 200
    mock_opensky.json.return_value = {
        "states": [
            ["abc123", "IBE123", "Spain", 1600000, 1600000, -3.7, 40.4, 9000.0, False, 220.0, 90.0, 0.0, None, 9100.0]
        ]
    }

    mock_get.side_effect = [mock_nominatim, mock_opensky]

    api = AeroplanesAPI()
    states = api.get_aeroplanes("Spain")
    assert len(states) == 1
    assert states[0][1] == "IBE123"


@patch("src.api.requests.get")
def test_get_aeroplanes_network_error(mock_get):
    mock_get.side_effect = requests.RequestException("Connection error")
    api = AeroplanesAPI()
    assert api.get_aeroplanes("Spain") == []
