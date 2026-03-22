import os
from typing import Any, Dict, List, Optional

import httpx


class ProkeralaAPI:
    def __init__(self) -> None:
        self.base_url = os.getenv("PROKERALA_BASE_URL", "https://api.prokerala.com")
        self.token_url = f"{self.base_url}/token"

        self.client_id = os.getenv("PROKERALA_CLIENT_ID")
        self.client_secret = os.getenv("PROKERALA_CLIENT_SECRET")

        self.natal_chart_endpoint = os.getenv(
            "PROKERALA_NATAL_ENDPOINT",
            "https://api.prokerala.com/v2/astrology/natal-planet-position",
        )

        self.default_latitude = float(os.getenv("DEFAULT_BIRTH_LATITUDE", "48.2082"))
        self.default_longitude = float(os.getenv("DEFAULT_BIRTH_LONGITUDE", "16.3738"))
        self.default_timezone = os.getenv("DEFAULT_BIRTH_TIMEZONE", "+01:00")

        self.timeout = float(os.getenv("PROKERALA_TIMEOUT_SECONDS", "20"))

    async def get_natal_chart(
        self,
        birth_date: str,
        birth_time: str,
        birth_city: str,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        timezone_offset: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        if not self.client_id or not self.client_secret:
            raise ValueError("PROKERALA_CLIENT_ID or PROKERALA_CLIENT_SECRET is not set")

        access_token = await self._get_access_token()
        if not access_token:
            return None

        lat = latitude if latitude is not None else self.default_latitude
        lon = longitude if longitude is not None else self.default_longitude
        tz = timezone_offset if timezone_offset else self.default_timezone

        params = self._build_natal_params(
            birth_date=birth_date,
            birth_time=birth_time,
            latitude=lat,
            longitude=lon,
            timezone_offset=tz,
        )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.natal_chart_endpoint,
                    headers=headers,
                    params=params,
                )

                if response.status_code != 200:
                    print("Prokerala natal chart error:", response.status_code, response.text)
                    return None

                raw_data = response.json()

                return self._normalize_natal_chart_response(
                    raw_data=raw_data,
                    birth_city=birth_city,
                    latitude=lat,
                    longitude=lon,
                    timezone_offset=tz,
                )

        except Exception as exc:
            print(f"Error fetching natal chart from Prokerala: {exc}")
            return None

    async def _get_access_token(self) -> Optional[str]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.token_url,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "application/json",
                    },
                )

                if response.status_code != 200:
                    print("Prokerala token error:", response.status_code, response.text)
                    return None

                data = response.json()
                return data.get("access_token")

        except Exception as exc:
            print(f"Error fetching Prokerala access token: {exc}")
            return None

    def _build_natal_params(
        self,
        birth_date: str,
        birth_time: str,
        latitude: float,
        longitude: float,
        timezone_offset: str,
    ) -> Dict[str, Any]:
        iso_datetime = f"{birth_date}T{birth_time}:00{timezone_offset}"

        return {
            "profile[datetime]": iso_datetime,
            "profile[coordinates]": f"{latitude:.2f},{longitude:.2f}",
            "house_system": "whole-sign",
            "orb": "default",
            "ayanamsa": 0,
            "la": "en",
        }

    def _normalize_natal_chart_response(
        self,
        raw_data: Dict[str, Any],
        birth_city: str,
        latitude: float,
        longitude: float,
        timezone_offset: str,
    ) -> Dict[str, Any]:
        data_node = raw_data.get("data", {}) if isinstance(raw_data.get("data"), dict) else {}

        planets = self._extract_planetary_positions(data_node)
        houses = self._extract_house_positions(data_node)
        ascendant_sign = self._extract_ascendant_sign(houses)

        sign_lookup = {
            item["name"].lower(): self._normalize_sign(item.get("sign"))
            for item in planets
        }

        return {
            "ascendant": ascendant_sign,
            "ascendant_sign": ascendant_sign,
            "sun_sign": sign_lookup.get("sun"),
            "moon_sign": sign_lookup.get("moon"),
            "mercury_sign": sign_lookup.get("mercury"),
            "venus_sign": sign_lookup.get("venus"),
            "mars_sign": sign_lookup.get("mars"),
            "jupiter_sign": sign_lookup.get("jupiter"),
            "saturn_sign": sign_lookup.get("saturn"),
            "planetary_positions": planets,
            "house_positions": houses,
            "provider_meta": {
                "provider": "prokerala",
                "birth_city": birth_city,
                "latitude": latitude,
                "longitude": longitude,
                "timezone_offset": timezone_offset,
            },
        }

    def _extract_planetary_positions(self, data_node: Dict[str, Any]) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []

        source = data_node.get("planet_positions", [])
        if not isinstance(source, list):
            return result

        for item in source:
            if not isinstance(item, dict):
                continue

            zodiac = item.get("zodiac", {}) if isinstance(item.get("zodiac"), dict) else {}
            zodiac_name = zodiac.get("name")

            result.append(
                {
                    "name": str(item.get("name", "")).strip().title(),
                    "sign": zodiac_name if zodiac_name else "Unknown",
                    "degree": self._to_float(item.get("degree")),
                    "house": self._to_int(item.get("house_number")),
                }
            )

        return result

    def _extract_house_positions(self, data_node: Dict[str, Any]) -> List[Dict[str, Any]]:
        result: List[Dict[str, Any]] = []

        source = data_node.get("houses", [])
        if not isinstance(source, list):
            return result

        for item in source:
            if not isinstance(item, dict):
                continue

            start_cusp = item.get("start_cusp", {}) if isinstance(item.get("start_cusp"), dict) else {}
            zodiac = start_cusp.get("zodiac", {}) if isinstance(start_cusp.get("zodiac"), dict) else {}
            zodiac_name = zodiac.get("name")

            result.append(
                {
                    "house": self._to_int(item.get("number")),
                    "sign": zodiac_name if zodiac_name else "Unknown",
                    "degree": self._to_float(start_cusp.get("degree")),
                }
            )

        return result

    def _extract_ascendant_sign(self, houses: List[Dict[str, Any]]) -> Optional[str]:
        for house in houses:
            if house.get("house") == 1:
                return self._normalize_sign(house.get("sign"))
        return None

    def _to_float(self, value: Any) -> Optional[float]:
        try:
            if value is None:
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    def _to_int(self, value: Any) -> Optional[int]:
        try:
            if value is None:
                return None
            return int(value)
        except (TypeError, ValueError):
            return None

    def _normalize_sign(self, value: Optional[str]) -> Optional[str]:
        if not value:
            return None

        value = str(value).strip().lower()

        aliases = {
            "aries": "aries",
            "taurus": "taurus",
            "gemini": "gemini",
            "cancer": "cancer",
            "leo": "leo",
            "virgo": "virgo",
            "libra": "libra",
            "scorpio": "scorpio",
            "sagittarius": "sagittarius",
            "capricorn": "capricorn",
            "aquarius": "aquarius",
            "pisces": "pisces",
        }

        return aliases.get(value)