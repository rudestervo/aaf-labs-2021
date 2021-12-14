from ExpressionNode import ExpressionNode

class StatementsNode(ExpressionNode):
    __codeStrings = []

    def __addNode(self, node):
        super().__init__()
        self.__codeStrings.append(node)
