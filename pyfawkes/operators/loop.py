import ast

from copy import deepcopy
from decorator import decorator


@decorator
def copy_node(mutate, node):
    return mutate(deepcopy(node, memo={id(node.parent): node.parent}))


class BreakContinueReplacement:
    def mutate_Break(node):
        yield ast.Continue()

    def mutate_Continue(node):
        yield ast.Break()


class ZeroIterationLoop:
    @copy_node
    def mutate_For_zero(node):
        node.body = [ast.Break(lineno=node.body[0].lineno)]
        yield node

    @copy_node
    def mutate_While_zero(node):
        node.body = [ast.Break(lineno=node.body[0].lineno)]
        yield node


class OneIterationLoop:
    @copy_node
    def mutate_For_one(node):
        node.body.append(ast.Break(lineno=node.body[-1].lineno + 1))
        yield node

    @copy_node
    def mutate_While_one(node):
        node.body.append(ast.Break(lineno=node.body[-1].lineno + 1))
        yield node


class ReverseIterationLoop:
    @copy_node
    def mutate_For_reverse(node):
        old_iter = node.iter
        node.iter = ast.Call(
            func=ast.Name(id=reversed.__name__, ctx=ast.Load()),
            args=[old_iter],
            keywords=[],
            starargs=None,
            kwargs=None,
        )
        yield node
