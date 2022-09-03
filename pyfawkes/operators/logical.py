import ast

from copy import deepcopy
from decorator import decorator


@decorator
def copy_node(mutate, node):
    return mutate(deepcopy(node, memo={id(node.parent): node.parent}))


class ConditionalOperatorNegation:
    @copy_node
    def yield_negated_test(node):
        node.test = ast.UnaryOp(op=ast.Not(), operand=node.test)
        yield node

    mutate_While = yield_negated_test
    mutate_If = yield_negated_test
    mutate_IfExp = yield_negated_test

    def mutate_In(node):
        yield ast.NotIn()

    def mutate_NotIn(node):
        yield ast.In()

    def mutate_Is(node):
        yield ast.IsNot()

    def mutate_IsNot(node):
        yield ast.Is()


class LogicalOperatorReplacement:
    def mutate_And(node):
        yield ast.Or()

    def mutate_Or(node):
        yield ast.And()


class BitwiseOperatorReplacement:
    def yield_other_bitoperators(node):
        for op in [ast.BitOr, ast.BitAnd, ast.BitXor]:
            if not isinstance(node, op):
                yield op()

    mutate_BitAnd = yield_other_bitoperators
    mutate_BitOr = yield_other_bitoperators
    mutate_BitXor = yield_other_bitoperators

    def mutate_LShift(node):
        yield ast.RShift()

    def mutate_RShift(node):
        yield ast.LShift()


class ComparisonOperatorReplacement:
    def yield_other_comparisons(node):
        for comp in [ast.Gt, ast.Lt, ast.GtE, ast.LtE, ast.Eq, ast.NotEq]:
            if not isinstance(node, comp):
                yield comp()

    mutate_Lt = yield_other_comparisons
    mutate_Gt = yield_other_comparisons
    mutate_LtE = yield_other_comparisons
    mutate_GtE = yield_other_comparisons
    mutate_Eq = yield_other_comparisons
    mutate_NotEq = yield_other_comparisons
