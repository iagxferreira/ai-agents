import pytest

from ai_agents.calculator import (
    CALCULATOR_TOOLS,
    add,
    calculate,
    divide,
    multiply,
    subtract,
)


@pytest.mark.parametrize(
    ("operation", "left", "right", "expected"),
    [
        (add, 2, 3, 5),
        (multiply, 2, 3, 6),
        (divide, 6, 3, 2),
        (subtract, 5, 3, 2),
    ],
)
def test_calculator_tools_perform_arithmetic(operation, left, right, expected) -> None:
    assert operation.invoke({"a": left, "b": right}) == expected


def test_calculator_tools_are_exposed_by_name() -> None:
    assert {tool.name for tool in CALCULATOR_TOOLS} == {
        "add",
        "multiply",
        "divide",
        "subtract",
        "calculate",
    }


def test_divide_by_zero_is_rejected() -> None:
    with pytest.raises(ZeroDivisionError):
        divide.invoke({"a": 1, "b": 0})


def test_calculate_preserves_operator_precedence() -> None:
    assert calculate.invoke({"expression": "9 * 6 + 3 / 4"}) == 54.75


def test_calculate_rejects_non_arithmetic_expressions() -> None:
    with pytest.raises(ValueError, match="unsupported expression"):
        calculate.invoke({"expression": "__import__('os').getcwd()"})
