"""BCD-коды и сложение для варианта A (8421) и остальных вариантов."""

from __future__ import annotations

from .common import ValidationError, decimal_string_add

BCD_TABLES: dict[str, dict[str, str]] = {
    "8421": {
        "0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100",
        "5": "0101", "6": "0110", "7": "0111", "8": "1000", "9": "1001",
    },
    "2421": {
        "0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100",
        "5": "1011", "6": "1100", "7": "1101", "8": "1110", "9": "1111",
    },
    "5421": {
        "0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100",
        "5": "1000", "6": "1001", "7": "1010", "8": "1011", "9": "1100",
    },
    "EXCESS-3": {
        "0": "0011", "1": "0100", "2": "0101", "3": "0110", "4": "0111",
        "5": "1000", "6": "1001", "7": "1010", "8": "1011", "9": "1100",
    },
    "GRAY": {
        "0": "0000", "1": "0001", "2": "0011", "3": "0010", "4": "0110",
        "5": "0111", "6": "0101", "7": "0100", "8": "1100", "9": "1101",
    },
}

DISPLAY_NAMES = {
    "8421": "8421 BCD (вариант A)",
    "2421": "2421 BCD",
    "5421": "5421 BCD",
    "EXCESS-3": "Excess-3",
    "GRAY": "Gray BCD",
}


class BCDService:
    """Сервис BCD-кодов."""

    @staticmethod
    def encode_number(number_text: str, variant: str = "8421") -> str:
        cleaned = number_text.strip()
        if not cleaned:
            raise ValidationError("Пустое число")
        if variant not in BCD_TABLES:
            raise ValidationError("Неизвестный BCD-вариант")
        table = BCD_TABLES[variant]
        groups = []
        for char in cleaned:
            if char not in table:
                raise ValidationError("BCD-сложение поддерживает только неотрицательные целые числа")
            groups.append(table[char])
        return " ".join(groups)

    @staticmethod
    def add_numbers(left_text: str, right_text: str, variant: str = "8421") -> dict[str, str]:
        result_decimal = decimal_string_add(left_text, right_text)
        return {
            "left_bcd": BCDService.encode_number(left_text, variant),
            "right_bcd": BCDService.encode_number(right_text, variant),
            "result_bcd": BCDService.encode_number(result_decimal, variant),
            "decimal_result": result_decimal,
            "variant": DISPLAY_NAMES[variant],
        }

    @staticmethod
    def build_report(left_text: str, right_text: str, variant: str = "8421") -> str:
        data = BCDService.add_numbers(left_text, right_text, variant)
        return (
            f"Код: {data['variant']}\n"
            f"A: {data['left_bcd']}\n"
            f"B: {data['right_bcd']}\n"
            f"Сумма (BCD): {data['result_bcd']}\n"
            f"Сумма (10):  {data['decimal_result']}"
        )
