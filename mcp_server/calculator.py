import re

def calculator(expression: str) -> str:
    """Evaluates a basic mathematical expression.
    
    Args:
        expression: The mathematical expression string (e.g. '70000 / 80').
        
    Returns:
        The calculation result as a string, or an error message.
    """
    # Clean expression and keep only safe math characters
    clean_expression = re.sub(r"[^0-9\+\-\*\/\(\)\. ]", "", expression)
    if clean_expression != expression:
        return f"Error: Expression contains invalid or unsafe characters. Supported characters: numbers, operators (+, -, *, /) and parentheses."
        
    try:
        result = eval(clean_expression, {"__builtins__": None}, {})
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression '{expression}': {str(e)}"
