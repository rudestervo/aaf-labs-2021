from ExpressionNode import ExpressionNode
from MyTokens.Token import Token


class AggregationNode(ExpressionNode):
    __aggregation = Token()
    __var = ExpressionNode()
    def __init__(self, aggregation, var):
        super().__init__()
        __aggregation = aggregation
        __var = var