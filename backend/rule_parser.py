import re
from .ast_node import Node

def parse_condition(condition):
    """Parse a condition string (e.g., 'age > 30' or 'department = "Sales"')"""
    pattern = r"(\w+)\s*(>|>=|<|<=|=|!=)\s*(\d+|'[^']+'|\"[^\"]*\")"
    match = re.match(pattern, condition)
    if match:
        key, operator, value = match.groups()
        return {key: f"{operator} {value.strip()}"}
    raise ValueError(f"Invalid condition: {condition}")

def create_rule(rule_string):
    """Convert the rule string into an AST"""
    # Tokenize the rule string
    tokens = re.findall(r"(\w+\s*(?:>|>=|<|<=|=|!=)\s*(?:\d+|'[^']+'|\"[^\"]*\"))|(\bAND\b|\bOR\b)", rule_string)
    
    # Flatten the list and filter out empty strings
    tokens = [token[0] or token[1] for token in tokens if token]

    stack = []
    
    print(f"Tokens: {tokens}")  # Debugging: print tokens

    i = 0
    while i < len(tokens):
        token = tokens[i]
        print(f"Current token: {token}")  # Debugging: print current token

        if re.match(r"\w+\s*(?:>|>=|<|<=|=|!=)\s*(?:\d+|'[^']+'|\"[^\"]*\")", token):
            # If the token is a valid condition
            parsed_condition = parse_condition(token)
            stack.append(Node(node_type="operand", value=parsed_condition))
            print(f"Added condition to stack: {parsed_condition}")
            print(f"Current stack after adding condition: {stack}")  # Debugging: print stack
        elif token in ["AND", "OR"]:
            if len(stack) < 2:
                # If there's only one operand in the stack, process the next token as a condition
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    if re.match(r"\w+\s*(?:>|>=|<|<=|=|!=)\s*(?:\d+|'[^']+'|\"[^\"]*\")", next_token):
                        parsed_condition = parse_condition(next_token)
                        stack.append(Node(node_type="operand", value=parsed_condition))
                        print(f"Added condition to stack: {parsed_condition}")
                        print(f"Current stack after adding condition: {stack}")  # Debugging: print stack
                        i += 1  # Skip the next token
                    else:
                        raise ValueError(f"Invalid condition: {next_token}")
                else:
                    raise ValueError(f"Not enough operands for operator '{token}'")
            print(f"Current stack before creating node for '{token}': {stack}")  # Debugging: print stack

            right = stack.pop()  # Right operand
            left = stack.pop()   # Left operand

            # Create a new operator node
            node = Node(node_type="operator", left=left, right=right, value=token)
            stack.append(node)  # Push the new node onto the stack
            print(f"Created node with operator '{token}' and added to stack: {node}")
            print(f"Current stack after creating node: {stack}")  # Debugging: print stack
        i += 1

    # Final validation of the stack
    if len(stack) != 1:
        raise ValueError(f"Failed to parse rule, remaining items in stack: {stack}")

    return stack[0]