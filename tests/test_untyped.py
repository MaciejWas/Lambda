from untyped.conversions import substitution
from untyped.data import Variable, Application, Abstraction, find_free_variables


def test_create():
    var1 = Variable(name="var1")
    var2 = Variable(name="var2")
    var3 = Variable(name="var3")
    appl = Application(
        of=var1,
        on=var2
    )
    abstr = Abstraction(
        bound_variable=var3,
        expression=appl
    )


def test_free_variables():
    var1 = Variable(name="var1")
    var2 = Variable(name="var2")
    var3 = Variable(name="var3")
    appl = Application(
        of=var1,
        on=var2
    )
    abstr = Abstraction(
        bound_variable=var3,
        expression=appl
    )

    free_vars = find_free_variables(abstr)

    assert any(map(
        lambda free_var: free_var.name == var1.name,
        free_vars
    ))

    assert any(map(
        lambda free_var: free_var.name == var2.name,
        free_vars
    ))

    assert all(map(
        lambda free_var: free_var.name != var3.name,
        free_vars
    ))


def test_substitution():
    var1 = Variable(name="var1")
    var2 = Variable(name="var2")
    var3 = Variable(name="var3")
    appl = Application(
        of=var1,
        on=var2
    )
    abstr = Abstraction(
        bound_variable=var3,
        expression=appl
    )

    abstr2 = substitution(abstr, var1, Variable("substituted"))
    assert isinstance(abstr2, Abstraction)



