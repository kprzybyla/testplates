from itertools import chain

from testplates import Mapping

MISSING = object()

MATCH_SIGN = " "
EXTRA_SIGN = "+"
MISSING_SIGN = "-"
MISMATCH_SIGN = "!"

OPEN_SIGN = "{"
CLOSE_SIGN = "}"
DIVIDER_SIGN = "|"

TEMPLATE = "{indent}{sign}   {key}: {diff}"


def pytest_assertrepr_compare(op, left, right):
    if not (isinstance(left, Mapping) and op == "=="):
        return None

    indent = 5 * " "

    lines = [f"{type(left).__name__} {OPEN_SIGN}"]

    for key in set(chain(left, right)):
        left_value = left.get(key, MISSING)
        right_value = right.get(key, MISSING)

        if left_value is MISSING:
            diff = f"{indent}{EXTRA_SIGN}   {key}: {right_value}"

        elif right_value is MISSING:
            diff = f"{indent}{MISSING_SIGN}   {key}: {left_value}"

        elif left_value != right_value:
            diff = f"{indent}{MISMATCH_SIGN}   {key}: {left_value} != {right_value}"

        else:
            diff = f"{indent}{MATCH_SIGN}   {key}: {left_value} == {right_value}"

        lines.append(diff)

    lines.append(f"{indent}{CLOSE_SIGN}")

    return lines


class Storage(dict):
    def __getattr__(self, item):
        return self[item]
