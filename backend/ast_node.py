class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # 'operator' or 'operand'
        self.left = left  # left child node
        self.right = right  # right child node
        self.value = value  # condition or operator

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, left={self.left}, right={self.right})"
