from untyped.conversions.alpha import alpha_conversion
from untyped.data.definitions import Application, Variable, LambdaTerm, Abstraction

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

    raise Exception('This should not have happened.')
