import re
from .ast_node import Node

def parse_condition(condition):
    """Parse a condition string (e.g., 'age > 30')"""
    pattern = r"(\w+)\s*(>|>=|<|<=|=|!=)\s*(\d+|'[^']+')"
    match = re.match(pattern, condition)
    if match:
        key, operator, value = match.groups()
        return {key: f"{operator} {value.strip()}"}
    raise ValueError(f"Invalid condition: {condition}")

def create_rule(rule_string):
    """Convert the rule string into an AST"""
    tokens = re.findall(r"\w+|[><=!]=?|['\w]+|\(|\)|AND|OR", rule_string)
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
            condition = parse_condition(token)
            stack.append(Node(node_type="operand", value=condition))
    
    while len(stack) > 1:
        stack.append(create_node())
    
    return stack[0]
