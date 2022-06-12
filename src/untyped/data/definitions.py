from dataclasses import dataclass
from itertools import chain
from typing import Union, Iterable, Any, Callable


@dataclass
class Variable:
    name: str

    def uniquify(self, suffix: str = "'") -> "Variable":
        return Variable(self.name + suffix)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Variable):
            return self.name == other.name

        return False

@dataclass
class Abstraction:
    bound_variable: Variable
    expression: "LambdaTerm"

@dataclass
class Application:
    of: "LambdaTerm"
    on: "LambdaTerm"

    def map(self, f: Callable[["LambdaTerm"], "LambdaTerm"]) -> "Application":
        return Application(
            f(self.of),
            f(self.on)
        )


ConstructionPrinciple = Union[Abstraction, Application]
LambdaTerm = Union[Variable, Abstraction, Application]


def find_subterms(term: LambdaTerm) -> Iterable[LambdaTerm]:
    match term:
        case Variable(name):
            return [term]
        case Application(of, on):
            return chain([term], find_subterms(of), find_subterms(on))
        case Abstraction(bound_var, expr):
            return chain([bound_var], find_subterms(expr))


def find_free_variables(term: LambdaTerm) -> Iterable[Variable]:
    match term:
        case Variable(name):
            return [term]
        case Application(of, on):
            return chain(find_free_variables(of), find_free_variables(on))
        case Abstraction(bound_var, expr):
            return filter(lambda var: var != bound_var, find_free_variables(expr))

