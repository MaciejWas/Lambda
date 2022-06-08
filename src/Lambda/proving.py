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
    term: LambdaTerm,
    replace: Variable,
    target: Variable,
    not_free_vars: list[Variable] = [],
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
                bound_var,
                alpha_reduction(expr, replace, target, not_free_vars + [bound_var]),
            )


def alpha_equiv(
    term1: LambdaTerm, term2: LambdaTerm, not_free_vars: list[Variable] = []
) -> bool:
    if type(term1) != type(term2):
        return False

    match term1:
        case Variable(name):
            return isinstance(term2, Variable)
        case Application(of, on):
            if isinstance(term2, Application):
                return alpha_equiv(of, term2.of, not_free_vars) and alpha_equiv(
                    on, term2.on, not_free_vars
                )
            return False
        case Abstraction(bound_var, expr):
            if isinstance(term2, Abstraction):
                expr2 = alpha_reduction(
                    term2.expression, term2.bound_variable, bound_var
                )
                return alpha_equiv(expr, expr2, not_free_vars + [bound_var])
            return False


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


x = Abstraction(Variable("XD"), Application(Variable("XD"), Variable(":o")))

print(alpha_reduction(x, Variable(":o"), Variable(":P")))
print(alpha_reduction(x, Variable("XD"), Variable(":P")))
