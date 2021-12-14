from ExpressionNode import ExpressionNode
from MyTokens.Token import Token

class VariableNode(ExpressionNode):
    __variable = Token()

    def __init__(self, variable):
        super().__init__()
        self.__variable = variable
