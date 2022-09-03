import ast

from pyfawkes import utils


class UnaryOperatorDeletion:
    def mutate_UnaryOp(node):
        yield node.operand


class StatementDeletion:
    def mutate_Assign(node):
        yield ast.Pass()

    def mutate_Return(node):
        yield ast.Pass()

    def mutate_Expr(node):
        if not utils.is_docstring(node.value):
            yield ast.Pass()
