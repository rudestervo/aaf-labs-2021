from ExpressionNode import ExpressionNode
from MyTokens.Token import Token


class UnarOperationNode(ExpressionNode):
    __operator = Token()
    __operand = ExpressionNode()

    def __init__(self, operator, operand):
        super().__init__()
        self.__operand = operand
        self.__operator = operator