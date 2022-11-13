from typing import Callable


def format_number(number: int) -> str:
    num = float(f"{number:.3g}")
    magnitude = 0

    format_human: Callable[[float], str] = lambda x: f"{x:f}".rstrip("0").rstrip(".")

    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0

    return f"{format_human(num)}{['', 'K', 'M', 'G', 'T', 'P'][magnitude]}"
