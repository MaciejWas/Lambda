from typing import Optional
from typing import Iterable, Union, Sequence
from itertools import chain
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Variable:
    name: str


@dataclass
class Abstraction:
    bound_variable: Variable
    expression: "LambdaTerm"


@dataclass
class Application:
    of: "LambdaTerm"
    on: "LambdaTerm"


ConstructionPrinciple = Union[Abstraction, Application]
LambdaTerm = Union[Variable, Abstraction, Application]


def alpha_reduction_inplace(term: LambdaTerm, replace: Variable, target: Variable):
    free_vars = find_free_variables(term)
    for var in free_vars:
        if var.name == replace.name:
            var.name = target.name


def alpha_reduction(
    term: LambdaTerm, replace: Variable, target: Variable, not_free_vars: list[Variable] = []
) -> LambdaTerm:
    match term:
        case Variable(name):
            if term == target:
                return replace
            return term
        case Application(of, on):
            return Application(
                alpha_reduction(of, replace, target, not_free_vars),
                alpha_reduction(on, replace, target, not_free_vars),
            )
        case Abstraction(bound_var, expr):
            return Abstraction(
                bound_var, alpha_reduction(expr, replace, target, not_free_vars + [bound_var])
            )
        case _:
            raise Exception("GUNWO KURWA MAC")

    term = deepcopy(term)
    alpha_reduction_inplace(term, replace, target)
    return term


def find_subterms(term: LambdaTerm) -> Iterable[LambdaTerm]:
    match term:
        case Variable(name):
            return [term]
        case Application(of, on):
            return chain([term], find_subterms(of), find_subterms(on))
        case Abstraction(bound_var, expr):
            return chain([bound_var], find_subterms(expr))
        case _:
            raise Exception("GUNWO KURWA MAC")


def find_free_variables(term: LambdaTerm) -> Iterable[Variable]:
    match term:
        case Variable(name):
            return [term]
        case Application(of, on):
            return chain(find_free_variables(of), find_free_variables(on))
        case Abstraction(bound_var, expr):
            return filter(lambda var: var != bound_var, find_free_variables(expr))
        case _:
            raise Exception("GUNWO KURWA MAC")


x = Abstraction(Variable("XD"), Application(Variable("XD"), Variable(":o")))

print(alpha_reduction(x, Variable(":o"), Variable(":P")))
print(alpha_reduction(x, Variable("XD"), Variable(":P")))
