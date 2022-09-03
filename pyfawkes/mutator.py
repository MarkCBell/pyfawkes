from collections import defaultdict
from contextlib import contextmanager
import ast
import re

from pyfawkes.operators import all_mixins
from pyfawkes.utils import notmutate

METHOD_PATTERN = re.compile(rf"mutate_([A-Za-z0-9]+)($|(_\w+)+$)")


class SiteMutation:
    def __init__(self, operator_abbr, node, new_node):
        self.operator_abbr = operator_abbr
        self.node = node
        self.new_node = new_node
        self.parent = self.node.parent
        for field, value in ast.iter_fields(self.parent):
            if isinstance(value, list):
                for index, child in enumerate(value):
                    if isinstance(child, ast.AST) and child == node:
                        self.parent_field = field
                        self.parent_index = index
                        self.parent_field_original = list(value)
            elif isinstance(value, ast.AST) and value == node:
                self.parent_field = field
                self.parent_index = None
                self.parent_field_original = value

    @contextmanager
    def __call__(self):
        if self.parent_index is None:
            if self.new_node is None:
                delattr(self.parent, self.parent_field)
            else:
                setattr(self.parent, self.parent_field, self.new_node)
            yield
            setattr(self.parent, self.parent_field, self.parent_field_original)
        else:
            if self.new_node is None:
                del getattr(self.parent, self.parent_field)[self.parent_index]
            else:
                getattr(self.parent, self.parent_field)[self.parent_index] = self.new_node
            yield
            setattr(self.parent, self.parent_field, self.parent_field_original)


def abbreviate(strn):
    return "".join(re.findall("[A-Z]", strn))


class Mutator(*all_mixins):
    def __init__(self, operator_abbreviations):
        self.transformers = defaultdict(list)
        for attr in dir(self):
            if match := METHOD_PATTERN.match(attr):
                method = getattr(self.__class__, attr)
                method.operator_abbr = abbreviate(method.__qualname__.split(".")[0])
                if method.operator_abbr in operator_abbreviations:
                    self.transformers[match.group(1)].append(method)
        print(sum(len(x) for x in self.transformers.values()))

    @classmethod
    def abbrs(cls):
        return {
            abbreviate(superclass.__name__): " ".join(word.lower() for word in re.findall("[A-Z][a-z]*", superclass.__name__))
            for superclass in cls.__mro__
            if superclass is not object
        }

    def explore(self, root):
        for node in ast.walk(root):
            if not hasattr(node, "not_mutate"):
                for transformer in self.transformers[node.__class__.__name__]:
                    for new_node in transformer(node):
                        ast.fix_missing_locations(new_node)
                        yield SiteMutation(transformer.operator_abbr, node, new_node)
