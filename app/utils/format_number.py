from typing import Callable


def format_number(number: int) -> str:
    num = float("{:.3g}".format(number))
    magnitude = 0

    format_human: Callable[[float], str] = (
        lambda x: "{:f}".format(x).rstrip("0").rstrip(".")
    )

    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0

    return "{}{}".format(format_human(num), ["", "K", "M", "G", "T", "P"][magnitude])
