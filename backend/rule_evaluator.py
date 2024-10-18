def evaluate_operand(operand, data):
    """Evaluate a single operand (condition)."""
    # Ensure operand is a Node and has the correct type
    if operand.type != "operand":
        raise ValueError("Expected operand type.")

    # Assuming operand.value is a dictionary for conditions
    condition = operand.value  # Expecting this to be a dictionary like {'key operator value'}
    key = list(condition.keys())[0]  # Get the key, which is the field name in data
    operator, value = condition[key].split(" ")  # Get operator and value from condition
    value = value.strip("'")  # Strip quotes from the value if necessary

    # Ensure the key exists in data
    if key not in data:
        raise KeyError(f"Key '{key}' not found in the provided data.")

    # Convert the value to the appropriate type for comparison
    try:
        if operator in (">", "<", "!="):
            value = int(value)  # Assuming numeric comparison for these operators
        elif operator == "=":
            value = str(value)  # Treat as string for equality check
    except ValueError:
        raise ValueError(f"Invalid value for comparison: {value}")

    # Evaluate the condition
    if operator == ">":
        return data[key] > value
    elif operator == "<":
        return data[key] < value
    elif operator == "=":
        return data[key] == value
    elif operator == "!=":
        return data[key] != value
    else:
        raise ValueError(f"Invalid operator: {operator}")



def evaluate_rule(ast, data):
    """Recursively evaluate an AST."""
    if ast is None:
        return False

    if ast.type == "operand":
        return evaluate_operand(ast, data)
    elif ast.type == "operator":
        left_eval = evaluate_rule(ast.left, data)
        right_eval = evaluate_rule(ast.right, data)
        if ast.value == "AND":
            return left_eval and right_eval
        elif ast.value == "OR":
            return left_eval or right_eval

    return False


