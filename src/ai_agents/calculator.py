import ast
import operator

from langchain_core.tools import tool


def _evaluate_expression(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
        }
        operation = operations.get(type(node.op))
        if operation is not None:
            return operation(
                _evaluate_expression(node.left), _evaluate_expression(node.right)
            )
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _evaluate_expression(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    raise ValueError("unsupported expression")


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    return a / b


@tool
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first number."""
    return a - b


@tool
def calculate(expression: str) -> float:
    """Evaluate an arithmetic expression with standard operator precedence."""
    try:
        tree = ast.parse(expression, mode="eval")
        return _evaluate_expression(tree.body)
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError) as error:
        if isinstance(error, ZeroDivisionError):
            raise
        raise ValueError("unsupported expression") from error


CALCULATOR_TOOLS = [add, multiply, divide, subtract, calculate]
