# SPDX-License-Identifier: MIT
# Copyright (c) 2026 WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from ._timezone_hint import TIMEZONE_HINT


type SpecificTime = (
    datetime
    | Literal["now"]
    | str
    | tuple[int, int, int, int, int, int]
)

type HourSystem = Literal["AM/PM", "24hr", "30hr"]
type Regnal = Literal["CE", "R.O.C.", "Japan"]
type ExportStyle = Literal[
    "Y/M/D H:M:S Zone hrs",
    "Y-M-D H:M:S Zone hrs",
    "YMD_HMS_Zone_Hrs",
    "ISO",
]


@dataclass(slots=True)
class Timestamp:
    """Store an aware datetime and export it in several timestamp formats."""

    time: SpecificTime = "now"
    _value: datetime = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._value = self._parse_time(self.time, zone="locale")

    @property
    def value(self) -> datetime:
        """Return the normalized, timezone-aware datetime."""
        return self._value

    def update(
        self,
        time: SpecificTime = "now",
        zone: TIMEZONE_HINT = "locale",
    ) -> None:
        """Update or reset the timestamp to a specific time."""
        self.time = time
        self._value = self._parse_time(time, zone)

    def export(
        self,
        zone: TIMEZONE_HINT = "locale",
        hrs: HourSystem = "24hr",
        /,
        *,
        regnal: Regnal = "CE",
        style: ExportStyle = "Y/M/D H:M:S Zone hrs",
    ) -> str:
        """Export this timestamp as a formatted string.

        R.O.C. output is always converted to Asia/Taipei.
        Japan output is always converted to Asia/Tokyo.
        Japanese ``30hr`` notation maps 00:00-05:59 to the previous
        date's 24:00-29:59 range.
        """
        self._validate_export_options(hrs=hrs, regnal=regnal, style=style)

        target_zone = self._regnal_zone(regnal) or zone
        value = self._convert_zone(self._value, target_zone)

        if style == "ISO":
            return value.isoformat(timespec="seconds")

        display_value, display_hour = self._display_value(value, hrs)
        date_text = self._format_date(display_value, regnal, style)
        time_text = self._format_time(display_value, hrs, display_hour)
        zone_name, offset_text = self._zone_parts(value, regnal)
        hour_label = self._hour_label(hrs, regnal)

        return self._compose(
            date_text=date_text,
            time_text=time_text,
            zone_name=zone_name,
            offset_text=offset_text,
            hour_label=hour_label,
            style=style,
        )

    @classmethod
    def _parse_time(
        cls,
        value: SpecificTime,
        zone: TIMEZONE_HINT,
    ) -> datetime:
        target_zone = cls._resolve_zone(zone)

        if value == "now":
            return (
                datetime.now().astimezone()
                if target_zone is None
                else datetime.now(target_zone)
            )

        if isinstance(value, datetime):
            parsed = value
        elif isinstance(value, tuple):
            parsed = datetime(*value)
        elif isinstance(value, str):
            try:
                parsed = datetime.fromisoformat(value)
            except ValueError as error:
                raise ValueError(
                    f"Unable to parse datetime string {value!r}; "
                    "use ISO 8601, for example "
                    "'2026-08-06T10:30:00+08:00'."
                ) from error
        else:
            raise TypeError(f"Unsupported time type: {type(value).__name__}")

        if parsed.tzinfo is None:
            # A naive clock time is interpreted in the requested zone.
            if target_zone is None:
                return parsed.astimezone()
            return parsed.replace(tzinfo=target_zone)

        if target_zone is None:
            return parsed

        return parsed.astimezone(target_zone)

    @staticmethod
    def _resolve_zone(zone: TIMEZONE_HINT) -> ZoneInfo | None:
        if zone == "locale":
            return None

        try:
            return ZoneInfo(zone)
        except ZoneInfoNotFoundError as error:
            raise ValueError(f"Unknown IANA timezone: {zone!r}") from error

    @classmethod
    def _convert_zone(
        cls,
        value: datetime,
        zone: TIMEZONE_HINT,
    ) -> datetime:
        target_zone = cls._resolve_zone(zone)
        return value.astimezone() if target_zone is None else value.astimezone(target_zone)

    @staticmethod
    def _regnal_zone(regnal: Regnal) -> TIMEZONE_HINT | None:
        if regnal == "R.O.C.":
            return "Asia/Taipei"  # type: ignore[return-value]
        if regnal == "Japan":
            return "Asia/Tokyo"  # type: ignore[return-value]
        return None

    @staticmethod
    def _validate_export_options(
        *,
        hrs: HourSystem,
        regnal: Regnal,
        style: ExportStyle,
    ) -> None:
        if hrs == "30hr" and regnal != "Japan":
            raise ValueError("30hr output is only supported with regnal='Japan'.")

        if style == "ISO" and (regnal != "CE" or hrs != "24hr"):
            raise ValueError(
                "ISO output requires regnal='CE' and hrs='24hr'."
            )

    @staticmethod
    def _display_value(
        value: datetime,
        hrs: HourSystem,
    ) -> tuple[datetime, int]:
        if hrs == "30hr" and value.hour < 6:
            return value - timedelta(days=1), value.hour + 24

        return value, value.hour

    @classmethod
    def _format_date(
        cls,
        value: datetime,
        regnal: Regnal,
        style: ExportStyle,
    ) -> str:
        if regnal == "R.O.C.":
            roc_year = value.year - 1911
            if roc_year <= 0:
                raise ValueError("R.O.C. dates before 1912 are not supported.")
            year_text = "元" if roc_year == 1 else str(roc_year)
            return f"民國{year_text}年{value.month}月{value.day}日"

        if regnal == "Japan":
            era_name, era_year = cls._japanese_era(value.date())
            year_text = "元" if era_year == 1 else str(era_year)
            return f"{era_name}{year_text}年{value.month}月{value.day}日"

        if style == "YMD_HMS_Zone_Hrs":
            return value.strftime("%Y%m%d")

        separator = "/" if style == "Y/M/D H:M:S Zone hrs" else "-"
        return f"{value.year:04d}{separator}{value.month:02d}{separator}{value.day:02d}"

    @staticmethod
    def _japanese_era(value: date) -> tuple[str, int]:
        eras = (
            (date(2019, 5, 1), "令和"),
            (date(1989, 1, 8), "平成"),
            (date(1926, 12, 25), "昭和"),
            (date(1912, 7, 30), "大正"),
            (date(1868, 1, 25), "明治"),
        )

        for start_date, era_name in eras:
            if value >= start_date:
                return era_name, value.year - start_date.year + 1

        raise ValueError("Japanese era output supports Meiji and later dates only.")

    @staticmethod
    def _format_time(
        value: datetime,
        hrs: HourSystem,
        display_hour: int,
    ) -> str:
        if hrs == "AM/PM":
            return value.strftime("%I:%M:%S %p")
        if hrs == "24hr":
            return value.strftime("%H:%M:%S")
        return f"{display_hour:02d}:{value.minute:02d}:{value.second:02d}"

    @staticmethod
    def _zone_parts(
        value: datetime,
        regnal: Regnal,
    ) -> tuple[str, str]:
        if regnal == "R.O.C.":
            zone_name = "臺北標準時間"
        elif regnal == "Japan":
            zone_name = "日本標準時"
        elif isinstance(value.tzinfo, ZoneInfo):
            zone_name = value.tzinfo.key
        else:
            zone_name = value.tzname() or "Unknown"

        offset = value.utcoffset()
        if offset is None:
            return zone_name, "UTC?"

        total_minutes = int(offset.total_seconds() // 60)
        sign = "+" if total_minutes >= 0 else "-"
        hours, minutes = divmod(abs(total_minutes), 60)
        offset_text = (
            f"UTC{sign}{hours}:{minutes:02d}"
            if minutes
            else f"UTC{sign}{hours}"
        )
        return zone_name, offset_text

    @staticmethod
    def _hour_label(hrs: HourSystem, regnal: Regnal) -> str:
        if regnal in {"R.O.C.", "Japan"}:
            return {
                "AM/PM": "12小時制",
                "24hr": "24小時制",
                "30hr": "30時間制",
            }[hrs]
        return hrs

    @staticmethod
    def _compose(
        *,
        date_text: str,
        time_text: str,
        zone_name: str,
        offset_text: str,
        hour_label: str,
        style: ExportStyle,
    ) -> str:
        if style == "YMD_HMS_Zone_Hrs":
            safe_zone = zone_name.replace("/", "-").replace(" ", "_")
            compact_time = time_text.replace(":", "").replace(" ", "_")
            return (
                f"{date_text}_{compact_time}_{safe_zone}_"
                f"{offset_text}_{hour_label}"
            )

        return (
            f"{date_text} {time_text} "
            f"{zone_name} ({offset_text}, {hour_label})"
        )