import re
from .ast_node import Node

# Define valid condition keys
VALID_CONDITIONS = {'age', 'department', 'income', 'spend'}

def parse_condition(condition):
    """Parse a condition string (e.g., 'age > 30')"""
    pattern = r"(\w+)\s*(>|>=|<|<=|=|!=)\s*(\d+|'[^']+')"
    match = re.match(pattern, condition)
    if match:
        key, operator, value = match.groups()
        # Validate the key against the valid conditions
        if key not in VALID_CONDITIONS:
            raise ValueError(f"Invalid condition: {key}")
        return {key: f"{operator} {value.strip()}"}
    raise ValueError(f"Invalid condition format: {condition}")

def create_rule(rule_string):
    """Convert the rule string into an AST"""
    # Update token extraction to ensure whole conditions are captured
    tokens = re.findall(r"\(?\s*\w+\s*(?:>|>=|<|<=|=|!=)\s*(?:\d+|'[^']+')\s*\)?|AND|OR", rule_string)
    stack = []

    def create_node():
        right = stack.pop()
        operator = stack.pop()
        left = stack.pop()
        return Node(node_type="operator", left=left, right=right, value=operator)

    for token in tokens:
        if token in ["AND", "OR"]:
            stack.append(token)
        elif re.match(r"\(", token):
            stack.append(token)
        elif re.match(r"\)", token):
            while len(stack) > 2:
                node = create_node()
                stack.append(node)
            stack.pop()  # pop '('
        else:
            try:
                # Parse the condition correctly
                condition = parse_condition(token.strip())
                stack.append(Node(node_type="operand", value=condition))
            except ValueError as e:
                raise ValueError(f"Failed to parse condition '{token}': {str(e)}")
    
    while len(stack) > 1:
        stack.append(create_node())
    
    return stack[0]
