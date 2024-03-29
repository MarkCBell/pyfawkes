import ast


class SliceIndexRemove:
    def mutate_Slice_remove_lower(node):
        if not node.lower:
            return

        yield ast.Slice(lower=None, upper=node.upper, step=node.step)

    def mutate_Slice_remove_upper(node):
        if not node.upper:
            return

        yield ast.Slice(lower=node.lower, upper=None, step=node.step)

    def mutate_Slice_remove_step(node):
        if not node.step:
            return

        yield ast.Slice(lower=node.lower, upper=node.upper, step=None)
