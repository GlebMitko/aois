# utils.py
"""Вспомогательные функции"""


def int_to_bits(n: int, width: int) -> list:
    """Число в список битов (MSB first)"""
    return [int(x) for x in format(n, f'0{width}b')]


def bits_to_int(bits: list) -> int:
    """Список битов в число"""
    return sum(bit << (len(bits) - 1 - i) for i, bit in enumerate(bits))


def print_truth_table(vars_list: list, rows: list, outputs: list):
    """Вывод таблицы истинности"""
    header = vars_list + outputs
    print(" | ".join(header))
    print("-" * (len(header) * 6))
    for i, row in enumerate(rows):
        vals = [str(row[v]) for v in vars_list] + [str(row[o]) for o in outputs]
        print(f"{i:2d}: " + " | ".join(vals))


def get_minterms(rows: list, output_name: str) -> list:
    """Получить минтермы для выхода"""
    return [i for i, row in enumerate(rows) if row.get(output_name) == 1]


def get_maxterms(rows: list, output_name: str, num_vars: int) -> list:
    """Получить макстермы для выхода"""
    all_indices = set(range(1 << num_vars))
    minterms = set(get_minterms(rows, output_name))
    return sorted(list(all_indices - minterms))


def build_sdnf(minterms: list, var_names: list) -> str:
    """Построить СДНФ по минтермам"""
    if not minterms:
        return "0"
    terms = []
    for mt in minterms:
        bits = int_to_bits(mt, len(var_names))
        literals = [var if b == 1 else f"!{var}" for b, var in zip(bits, var_names)]
        terms.append('&'.join(literals))
    return ' | '.join(terms)


def build_sknf(maxterms: list, var_names: list) -> str:
    """Построить СКНФ по макстермам"""
    if not maxterms:
        return "1"
    terms = []
    for mt in maxterms:
        bits = int_to_bits(mt, len(var_names))
        literals = [f"!{var}" if b == 1 else var for b, var in zip(bits, var_names)]
        terms.append(f"({' | '.join(literals)})")
    return ' & '.join(terms)


def to_not_and_or(sdnf_expr: str) -> str:
    """Преобразовать СДНФ в базис НЕ-И-ИЛИ (по закону де Моргана)"""
    if not sdnf_expr or sdnf_expr == "0":
        return "0"
    if sdnf_expr == "1":
        return "1"

    if ' | ' not in sdnf_expr:
        if sdnf_expr.startswith('!'):
            return f"!({sdnf_expr[1:]})"
        return sdnf_expr

    terms = sdnf_expr.split(' | ')
    not_terms = []
    for t in terms:
        if '&' in t:
            not_terms.append(f"!({t})")
        else:
            not_terms.append(f"!{t}")

    if len(not_terms) == 1:
        return not_terms[0]
    return f"!({' & '.join(not_terms)})"