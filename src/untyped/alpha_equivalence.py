from typing import Optional, List
from untyped.alpha import alpha_conversion
from untyped.definitions import Application, Variable, LambdaTerm, Abstraction


def is_alpha_equivalent(
        term1: LambdaTerm, term2: LambdaTerm, bounded_vars: Optional[List[Variable]] = None
) -> bool:
    if bounded_vars is None:
        bounded_vars = []

    if type(term1) != type(term2):
        return False

    match term1:
        case Variable(name):
            assert isinstance(term2, type(term1))
            if name in bounded_vars:
                return term2.name == name
            return True

        case Application(of, on):
            assert isinstance(term2, type(term1))
            return is_alpha_equivalent(of, term2.of, bounded_vars) and is_alpha_equivalent(on, term2.on, bounded_vars)

        case Abstraction(bound_var, expr):
            assert isinstance(term2, type(term1))
            other_bound_var = term2.bound_variable
            other_expr = term2.expression

            # We convert the other abstraction to have the same bound variable
            converted_other_expr = alpha_conversion(other_expr, other_bound_var, bound_var)

            return is_alpha_equivalent(expr, converted_other_expr, bounded_vars + [bound_var])

    raise Exception('This should not have happened.')
