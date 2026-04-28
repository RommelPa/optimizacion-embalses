from __future__ import annotations

from datetime import datetime


def format_text(value: object, empty_text: str = "-") -> str:
    if value is None:
        return empty_text

    text = str(value).strip()
    return text if text else empty_text


def format_int(value: object) -> str:
    if value is None:
        return "-"

    try:
        return str(int(float(str(value))))
    except (ValueError, TypeError):
        return str(value)


def format_number(
    value: float | int | str | None,
    decimals: int = 2,
) -> str:
    if value is None:
        return "-"

    try:
        return f"{float(value):,.{decimals}f}"
    except (ValueError, TypeError):
        return str(value)


def format_sequence_stat(
    values: list[float],
    stat: str,
    decimals: int = 3,
) -> str:
    if not values:
        return "-"

    if stat == "min":
        return format_number(min(values), decimals)
    if stat == "max":
        return format_number(max(values), decimals)
    if stat == "avg":
        return format_number(sum(values) / len(values), decimals)

    return "-"


def format_datetime_display(value: object) -> str:
    if value is None:
        return "-"

    text = str(value).strip()
    if not text:
        return "-"

    try:
        iso_text = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso_text)
        return dt.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return text