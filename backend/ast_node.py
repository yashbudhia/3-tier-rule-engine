class Node:
    def __init__(self, type: str, value: str, left: 'Node' = None, right: 'Node' = None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    # Serialize the Node to a dictionary
    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }

    # Deserialize a dictionary to a Node
    @staticmethod
    def from_dict(data):
        if data is None:
            return None
        return Node(
            type=data['type'],
            value=data['value'],
            left=Node.from_dict(data['left']),
            right=Node.from_dict(data['right'])
        )

    def get_operands(self):
        """Retrieve all operand nodes from the AST."""
        operands = []

        # If this node is an operand, add it to the list
        if self.type == "operand":
            operands.append(self)

        # Traverse the left and right children, if they exist
        if self.left:
            operands.extend(self.left.get_operands())
        if self.right:
            operands.extend(self.right.get_operands())

        return operands
