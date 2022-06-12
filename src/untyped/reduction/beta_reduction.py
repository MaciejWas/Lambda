from untyped.conversions import substitution
from untyped.data import Application, LambdaTerm, Variable, Abstraction


def _handle_application_beta_reduction(appl: Application):
    match appl.of:
        case Variable(_name):
            return appl
        case Application(_of, _on):
            return appl


def one_step_beta_reduction(term: LambdaTerm) -> LambdaTerm:
    match term:
        case Variable(name):
            return term
        case Application(of, on):
            return _handle_application_beta_reduction(term)
        case Abstraction(bound_var, expr):
            return substitution(term, bound_var, expr)


def do_application(appl: Application) -> LambdaTerm:
    match appl.of:
        case Variable(_):
            return appl
        case Abstraction(bound_variable, expression):
            return substitution(appl.on, bound_variable, expression)
        case Application(_, _):
            return do_application(Application(
                beta_reduction(appl.of),
                beta_reduction(appl.on)
            ))
