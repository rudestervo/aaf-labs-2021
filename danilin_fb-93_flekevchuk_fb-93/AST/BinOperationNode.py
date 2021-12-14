from ExpressionNode import ExpressionNode
from MyTokens.Token import Token

class BinOperationNode(ExpressionNode):
    __operation = Token()
    __leftNode = ExpressionNode()
    __rightNode = ExpressionNode()
    def __init__(self, operation, leftNode, rightNode):
        super().__init__()
        self.__operation = operation
        self.__leftNode = leftNode
        self.__rightNode = rightNode

