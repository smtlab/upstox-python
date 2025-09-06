import sys
import types
import unittest
from datetime import date
from unittest.mock import MagicMock

# The package imports a number of optional dependencies during initialisation
# (websocket and protobuf based streamers). Those packages are not available in
# the test environment, so we register lightweight stubs before importing the
# client package to avoid import errors.
sys.modules.setdefault("websocket", MagicMock())

feeder_pkg = types.ModuleType("feeder")
sys.modules["upstox_client.feeder"] = feeder_pkg

md_stub = types.ModuleType("market_data_streamer")
md_stub.MarketDataStreamer = object
sys.modules["upstox_client.feeder.market_data_streamer"] = md_stub

md_v3_stub = types.ModuleType("market_data_streamer_v3")
md_v3_stub.MarketDataStreamerV3 = object
sys.modules["upstox_client.feeder.market_data_streamer_v3"] = md_v3_stub

portfolio_stub = types.ModuleType("portfolio_data_streamer")
portfolio_stub.PortfolioDataStreamer = object
sys.modules["upstox_client.feeder.portfolio_data_streamer"] = portfolio_stub

from upstox_client.historical_client import HistoricalDataClient


class TestHistoricalDataClient(unittest.TestCase):
    def test_get_historical_data_formats_dates_and_calls_api(self):
        history_api = MagicMock()
        client = HistoricalDataClient(history_api=history_api)

        client.get_historical_data(
            "NSE_EQ|TEST",
            "day",
            date(2024, 1, 1),
            date(2024, 1, 31),
        )

        history_api.get_historical_candle_data1.assert_called_once_with(
            "NSE_EQ|TEST",
            "day",
            "2024-01-31",
            "2024-01-01",
            "v2",
        )


if __name__ == "__main__":
    unittest.main()
