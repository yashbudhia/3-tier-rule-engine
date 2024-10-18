from .ast_node import Node

def combine_rules(rules, operator="AND"):
    """Combine multiple ASTs into one using AND/OR operator."""
    if not rules:
        return None

    # Validate operator
    if operator not in ("AND", "OR"):
        raise ValueError(f"Invalid operator: {operator}. Use 'AND' or 'OR'.")

    combined_root = rules[0]

    # Check if the first rule is a valid Node
    if not isinstance(combined_root, Node):
        raise TypeError("The first rule must be an instance of Node.")

    for rule in rules[1:]:
        if not isinstance(rule, Node):
            raise TypeError(f"Each rule must be an instance of Node, but got {type(rule).__name__}.")
        
        # Use 'type' instead of 'node_type' to match the Node class definition
        combined_root = Node(type="operator", left=combined_root, right=rule, value=operator)

    return combined_root
