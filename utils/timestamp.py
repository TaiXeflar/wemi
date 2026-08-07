
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# SPDX-License-Identifier: MIT
# Copyright (c) 2026 WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Literal, TypeAlias
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from ._timezone_hint import TIMEZONE_HINT


SpecificTime: TypeAlias = (
    datetime
    | Literal["now"]
    | str
    | tuple[int, int, int, int, int, int]
)
HourSystem: TypeAlias = Literal["AM/PM", "24hr", "30hr"]
Regnal: TypeAlias = Literal["CE", "R.O.C.", "Japan"]
ExportStyle: TypeAlias = Literal[
    "Y/M/D H:M:S Zone hrs",
    "Y-M-D H:M:S Zone hrs",
    "YMD_HMS_Zone_Hrs",
    "ISO",
]


@dataclass(slots=True)
class Timestamp:
    time: SpecificTime = "now"
    _value: datetime = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._value = self._parse(self.time, "locale")

    @property
    def value(self) -> datetime:
        return self._value

    def update(
        self,
        time: SpecificTime = "now",
        zone: TIMEZONE_HINT = "locale",
    ) -> None:
        self.time = time
        self._value = self._parse(time, zone)

    def export(
        self,
        zone: TIMEZONE_HINT = "locale",
        hrs: HourSystem = "24hr",
        /,
        *,
        regnal: Regnal = "CE",
        style: ExportStyle = "Y/M/D H:M:S Zone hrs",
    ) -> str:
        # 紀年直接決定輸出地區；CE 才使用呼叫端指定的 zone。
        if regnal == "R.O.C.":
            zone = "Asia/Taipei"
        elif regnal == "Japan":
            zone = "Asia/Tokyo"

        if hrs == "30hr" and regnal != "Japan":
            raise ValueError("hrs='30hr' requires regnal='Japan'.")

        value = self._to_zone(self._value, zone)

        if style == "ISO":
            if regnal != "CE" or hrs != "24hr":
                raise ValueError("style='ISO' requires regnal='CE' and hrs='24hr'.")
            return value.isoformat(timespec="seconds")

        display_value = value
        display_hour = value.hour
        if hrs == "30hr" and value.hour < 6:
            display_value = value - timedelta(days=1)
            display_hour += 24

        date_text = self._format_date(display_value, regnal, style)
        time_text = self._format_time(display_value, hrs, display_hour)
        zone_name = self._zone_name(value, zone, regnal)
        offset_text = self._utc_offset(value)
        hour_text = self._hour_text(hrs, regnal)

        if style == "YMD_HMS_Zone_Hrs":
            return "_".join(
                (
                    date_text,
                    time_text.replace(":", "").replace(" ", "_"),
                    zone_name.replace("/", "-").replace(" ", "_"),
                    offset_text,
                    hour_text,
                )
            )

        return f"{date_text} {time_text} {zone_name} ({offset_text}, {hour_text})"

    @classmethod
    def _parse(cls, value: SpecificTime, zone: TIMEZONE_HINT) -> datetime:
        tz = cls._get_zone(zone)

        if value == "now":
            return datetime.now(tz) if tz is not None else datetime.now().astimezone()

        if isinstance(value, datetime):
            parsed = value
        elif isinstance(value, tuple):
            if len(value) != 6:
                raise ValueError("time tuple must be (year, month, day, hour, minute, second).")
            parsed = datetime(*value)
        elif isinstance(value, str):
            try:
                parsed = datetime.fromisoformat(value)
            except ValueError as error:
                raise ValueError(f"invalid ISO 8601 datetime: {value!r}") from error
        else:
            raise TypeError(f"unsupported time type: {type(value).__name__}")

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=tz) if tz is not None else parsed.astimezone()
        return parsed.astimezone(tz) if tz is not None else parsed

    @staticmethod
    def _get_zone(zone: TIMEZONE_HINT) -> ZoneInfo | None:
        if zone == "locale":
            return None
        try:
            return ZoneInfo(zone)
        except ZoneInfoNotFoundError as error:
            raise ValueError(f"unknown IANA timezone: {zone!r}") from error

    @classmethod
    def _to_zone(cls, value: datetime, zone: TIMEZONE_HINT) -> datetime:
        tz = cls._get_zone(zone)
        return value.astimezone(tz) if tz is not None else value.astimezone()

    @classmethod
    def _format_date(
        cls,
        value: datetime,
        regnal: Regnal,
        style: ExportStyle,
    ) -> str:
        if regnal == "R.O.C.":
            year = value.year - 1911
            if year < 1:
                raise ValueError("R.O.C. dates before 1912 are not supported.")
            return f"民國{'元' if year == 1 else year}年{value.month}月{value.day}日"

        if regnal == "Japan":
            era, year = cls._japanese_era(value.date())
            return f"{era}{'元' if year == 1 else year}年{value.month}月{value.day}日"

        if style == "YMD_HMS_Zone_Hrs":
            return value.strftime("%Y%m%d")

        separator = "/" if style == "Y/M/D H:M:S Zone hrs" else "-"
        return value.strftime(f"%Y{separator}%m{separator}%d")

    @staticmethod
    def _japanese_era(value: date) -> tuple[str, int]:
        eras = (
            (date(2019, 5, 1), "令和"),
            (date(1989, 1, 8), "平成"),
            (date(1926, 12, 25), "昭和"),
            (date(1912, 7, 30), "大正"),
            (date(1868, 1, 25), "明治"),
        )
        for start, name in eras:
            if value >= start:
                return name, value.year - start.year + 1
        raise ValueError("Japanese era output supports Meiji and later dates only.")

    @staticmethod
    def _format_time(value: datetime, hrs: HourSystem, hour: int) -> str:
        if hrs == "AM/PM":
            return value.strftime("%I:%M:%S %p")
        if hrs == "24hr":
            return value.strftime("%H:%M:%S")
        return f"{hour:02d}:{value.minute:02d}:{value.second:02d}"

    @staticmethod
    def _zone_name(value: datetime, zone: TIMEZONE_HINT, regnal: Regnal) -> str:
        if regnal == "R.O.C.":
            return "臺北標準時間"
        if regnal == "Japan":
            return "日本標準時"
        if zone != "locale":
            return zone
        return getattr(value.tzinfo, "key", None) or value.tzname() or "locale"

    @staticmethod
    def _utc_offset(value: datetime) -> str:
        offset = value.utcoffset()
        if offset is None:
            return "UTC?"
        minutes = int(offset.total_seconds() // 60)
        sign = "+" if minutes >= 0 else "-"
        hours, remainder = divmod(abs(minutes), 60)
        return f"UTC{sign}{hours}:{remainder:02d}" if remainder else f"UTC{sign}{hours}"

    @staticmethod
    def _hour_text(hrs: HourSystem, regnal: Regnal) -> str:
        if regnal == "R.O.C.":
            return "12小時制" if hrs == "AM/PM" else "24小時制"
        if regnal == "Japan":
            return {
                "AM/PM": "12時間制",
                "24hr": "24時間制",
                "30hr": "30時間制",
            }[hrs]
        return hrs
