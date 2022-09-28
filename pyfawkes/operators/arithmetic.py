import ast


class ArithmeticOperatorReplacement:
    def yield_other_binary_operators(node):
        for op in [ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow]:
            if not isinstance(node, op):
                yield op()

    mutate_Add = yield_other_binary_operators
    mutate_Sub = yield_other_binary_operators
    mutate_Mult = yield_other_binary_operators
    mutate_Div = yield_other_binary_operators
    mutate_FloorDiv = yield_other_binary_operators
    mutate_Mod = yield_other_binary_operators
    mutate_Pow = yield_other_binary_operators
