from typing import Optional

from untyped.data.definitions import LambdaTerm, find_free_variables, Variable, Application, Abstraction


def alpha_conversion_inplace(term: LambdaTerm, replace: Variable, target: Variable):
    """See alpha_conversion"""

    free_vars = find_free_variables(term)
    for var in free_vars:
        if var.name == replace.name:
            var.name = target.name


def alpha_conversion(
    term: LambdaTerm,
    old: Variable,
    new: Variable,
    not_free_vars: Optional[list[Variable]] = None,
) -> LambdaTerm:
    """Renaming the bound variables in the expression. Used to avoid name collisions.
     source: en.wikipedia.org/wiki/Lambda_calculus"""

    if not_free_vars is None:
        not_free_vars = []

    match term:
        case Variable(name):
            if term == old:
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


def substitution(term: LambdaTerm, old: Variable, new: LambdaTerm) -> LambdaTerm:
    """Substitutes old for new"""

    match term:
        case Variable(_):
            return new if term == old else term
        case Application(of, on):
            return Application(
                substitution(of, old, new),
                substitution(on, old, new)
            )
        case Abstraction(bound_var, expr):
            if bound_var == old:
                new_bound_var = bound_var.uniquify()
                new_expr = alpha_conversion(expr, bound_var, new_bound_var)
                return substitution(Abstraction(new_bound_var, new_expr), old, new)

            return Abstraction(
                bound_var,
                substitution(expr, old, new)
            )
