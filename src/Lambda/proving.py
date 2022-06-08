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


def alpha_conversion_inplace(term: LambdaTerm, replace: Variable, target: Variable):
    free_vars = find_free_variables(term)
    for var in free_vars:
        if var.name == replace.name:
            var.name = target.name


def alpha_conversion(
    term: LambdaTerm,
    old: Variable,
    new: Variable,
    not_free_vars: list[Variable] = [],
) -> LambdaTerm:
    match term:
        case Variable(name):
            if name == old.name:
                return new
            return term
        case Application(of, on):
            return Application(
                alpha_conversion(of, old, new, not_free_vars),
                alpha_conversion(on, old, new, not_free_vars),
            )
        case Abstraction(bound_var, expr):
            return Abstraction(
                bound_var,
                alpha_conversion(expr, old, new, not_free_vars + [bound_var]),
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
                expr2 = alpha_conversion(
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


def substitution(term: LambdaTerm, var: Variable, target: LambdaTerm) -> LambdaTerm:
    match term:
        case Variable(name):
            return target if name == var.name else term
        case Application(of, on):
            return Application(
                substitution(of, var, target),
                substitution(on, var, target)
            )
        case Abstraction(bound_var, expr):
            if bound_var.name == var.name:
                new_bound_var = Variable(bound_var.name + "'")
                new_expr = alpha_conversion(expr, bound_var, new_bound_var)
                return substitution(Abstraction(new_bound_var, new_expr), var, target)

            return Abstraction(
                bound_var,
                substitution(expr, var, target)
            )



x = Abstraction(Variable("XD"), Application(Variable("XD"), Variable(":o")))
y = Abstraction(Variable("XDD"), Application(Variable("XDD"), Variable(":p")))

print(alpha_conversion(x, Variable(":o"), Variable(":P")))
print(alpha_conversion(x, Variable("XD"), Variable(":P")))
print(alpha_equiv(x, y))
print(substitution(x, Variable("XD"), Variable("SUBSFSDFASD")))
print(substitution(x, Variable(":o"), Variable("SUBSFSDFASD")))



