from .ast_node import Node

def combine_rules(rules, operator="AND"):
    """Combine multiple ASTs into one using AND/OR operator"""
    if not rules:
        return None
    combined_root = rules[0]
    for rule in rules[1:]:
        combined_root = Node(node_type="operator", left=combined_root, right=rule, value=operator)
    return combined_root
