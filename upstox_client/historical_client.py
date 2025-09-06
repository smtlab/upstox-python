"""Utilities for fetching historical candle data.

This module provides a small wrapper around :class:`~upstox_client.api.history_api.HistoryApi`
that exposes a simpler interface for fetching historical candle data.

Example
-------

>>> from upstox_client import ApiClient, Configuration
>>> from upstox_client.historical_client import HistoricalDataClient
>>> config = Configuration()
>>> config.access_token = "ACCESS_TOKEN"
>>> client = HistoricalDataClient(ApiClient(config))
>>> candles = client.get_historical_data("NSE_EQ|INE669E01016", "day", "2024-01-01", "2024-01-31")
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional, Union

from .api.history_api import HistoryApi
from .api_client import ApiClient

DateType = Union[str, date, datetime]


class HistoricalDataClient:
    """Simple client for the historical candle data endpoints."""

    def __init__(self, api_client: Optional[ApiClient] = None, api_version: str = "v2", history_api: Optional[HistoryApi] = None):
        """Create a new :class:`HistoricalDataClient` instance.

        Parameters
        ----------
        api_client:
            Optional :class:`~upstox_client.api_client.ApiClient` instance. If not
            provided a default instance will be created.
        api_version:
            API version header to be used when making requests. Defaults to ``"v2"``.
        history_api:
            Internal use only. Allows injecting a custom :class:`HistoryApi` instance,
            primarily for testing.
        """

        self._history_api = history_api or HistoryApi(api_client or ApiClient())
        self._api_version = api_version

    @staticmethod
    def _format_date(value: DateType) -> str:
        """Format ``value`` into the ``YYYY-MM-DD`` string expected by the API."""
        if isinstance(value, (date, datetime)):
            return value.strftime("%Y-%m-%d")
        return str(value)

    def get_historical_data(self, instrument_key: str, interval: str, from_date: DateType, to_date: DateType):
        """Fetch historical candle data for ``instrument_key``.

        Parameters
        ----------
        instrument_key:
            Instrument identifier.
        interval:
            Interval between candles. For example ``"day"`` or ``"1minute"``.
        from_date:
            Start date of the range (inclusive). Accepts ``datetime.date``, ``datetime.datetime``
            or an ISO formatted string ``YYYY-MM-DD``.
        to_date:
            End date of the range (inclusive). Accepts the same formats as ``from_date``.

        Returns
        -------
        :class:`~upstox_client.models.get_historical_candle_response.GetHistoricalCandleResponse`
            Response object returned by the underlying API client.
        """
        from_str = self._format_date(from_date)
        to_str = self._format_date(to_date)
        return self._history_api.get_historical_candle_data1(
            instrument_key,
            interval,
            to_str,
            from_str,
            self._api_version,
        )
