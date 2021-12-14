from ExpressionNode import ExpressionNode
from MyTokens.Token import Token

class NumberNode(ExpressionNode):
    __number = Token()

    def __init__(self, number):
        super().__init__()
        __number = number
    
