from typing import Optional, List

from untyped.definitions import LambdaTerm, find_free_variables, Variable, Application, Abstraction


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
) -> LambdaTerm:
    """Renaming the bound variables in the expression. Used to avoid name collisions.
     source: en.wikipedia.org/wiki/Lambda_calculus"""
    return substitution(term, old, new)


def substitution(term: LambdaTerm, old: Variable, new: LambdaTerm, bounded_variables: Optional[List[Variable]] = None) -> LambdaTerm:
    """Substitutes old for new"""

    if bounded_variables is None:
        bounded_variables = []

    match term:
        case Variable(_):
            assert term not in bounded_variables, f"Error in implementation. {term} should be renamed before it is " \
                                                  "reached. "
            return new if term == old else term

        case Application(of, on):
            return Application(
                substitution(of, old, new),
                substitution(on, old, new)
            )
        case Abstraction(bound_var, expr):
            assert bound_var not in bounded_variables, f"Badly constructed lambda expression. {bound_var} is already " \
                                                       "bounded. "
            if bound_var == old:
                new_bound_var = bound_var.uniquify()
                while bound_var in bounded_variables:
                    new_bound_var = bound_var.uniquify()

                new_expr = substitution(expr, bound_var, new_bound_var)
                new_term = Abstraction(new_bound_var, new_expr)
                return substitution(new_term, old, new)

            return Abstraction(
                bound_var,
                substitution(expr, old, new)
            )
