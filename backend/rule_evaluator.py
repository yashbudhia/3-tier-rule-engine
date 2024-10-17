def evaluate_operand(operand, data):
    """Evaluate a single operand (condition)"""
    key, condition = list(operand.items())[0]
    operator, value = condition.split(" ")
    value = value.strip("'")
    
    if operator == ">":
        return data[key] > int(value)
    elif operator == "<":
        return data[key] < int(value)
    elif operator == "=":
        return data[key] == value
    elif operator == "!=":
        return data[key] != value
    # Add more conditions if necessary
    return False

def evaluate_rule(ast, data):
    """Recursively evaluate an AST"""
    if ast.type == "operand":
        return evaluate_operand(ast.value, data)
    elif ast.type == "operator":
        left_eval = evaluate_rule(ast.left, data)
        right_eval = evaluate_rule(ast.right, data)
        if ast.value == "AND":
            return left_eval and right_eval
        elif ast.value == "OR":
            return left_eval or right_eval
    return False
