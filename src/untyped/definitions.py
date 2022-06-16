from dataclasses import dataclass
from itertools import chain
from typing import Union, Any, Callable, Set, Iterable


@dataclass
class Variable:
    name: str

    def uniquify(self, suffix: str = "'") -> "Variable":
        """Not in place!"""

        return Variable(self.name + suffix)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Variable):
            return self.name == other.name

        return False

    def __hash__(self) -> int:
        return hash(self.name)


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


def find_variables(term: LambdaTerm) -> Iterable[Variable]:
    match term:
        case Variable(name):
            yield term
        case Application(of, on):
            return chain(find_variables(of), find_variables(on))
        case Abstraction(bound_var, expr):
            yield bound_var
            return find_variables(expr)


def find_subterms(term: LambdaTerm) -> Set[LambdaTerm]:
    match term:
        case Variable(name):
            return {term}
        case Application(of, on):
            return {term}.union(find_subterms(of)).union(find_subterms(on))
        case Abstraction(bound_var, expr):
            return {bound_var}.union(find_subterms(expr))


def find_free_variables(term: LambdaTerm) -> Set[Variable]:
    match term:
        case Variable(name):
            return {term}
        case Application(of, on):
            return find_free_variables(of).union(find_free_variables(on))
        case Abstraction(bound_var, expr):
            return set(filter(lambda var: var != bound_var, find_free_variables(expr)))
