import ast


class ArithmeticOperatorReplacement:
    def mutate_Add(node):
        yield ast.Sub()

    def mutate_Sub(node):
        yield ast.Add()

    def mutate_Mult(node):
        yield ast.Div()
        yield ast.FloorDiv()
        yield ast.Pow()

    def mutate_Div(node):
        yield ast.Mult()
        yield ast.FloorDiv()

    def mutate_FloorDiv(node):
        yield ast.Div()
        yield ast.Mult()

    def mutate_Mod(node):
        yield ast.Mult()

    def mutate_Pow(node):
        yield ast.Mult()

    def mutate_USub(node):
        yield ast.UAdd()

    def mutate_UAdd(node):
        yield ast.USub()
