from untyped.definitions import *
from untyped.alpha import *


def assert_eq_iterable(it1: Iterable, it2: Iterable):
    shared = set()
    for x in it1:
        assert x in it2
        shared.add(x)
    for x in it2:
        if x not in shared:
            assert x in it1


def make_variables(text: str) -> List[Variable]:
    return [Variable(name) for name in text.split(" ")]


def test_create():
    a, b, c, d = make_variables("a b c d")

    ab = Application(
        of=a,
        on=b
    )
    cab = Application(
        of=c,
        on=ab
    )
    cab = Application(
        of=cab,
        on=d
    )

    Abstraction(
        bound_variable=d,
        expression=cab
    )


def test_free_variables_0():
    a, b, c, d = make_variables("a b c d")
    assert_eq_iterable(find_free_variables(a), [a])

    ab = Application(a, b)
    assert_eq_iterable(find_free_variables(ab), [a, b])

    a_b = Abstraction(a, b)
    assert_eq_iterable(find_free_variables(a_b), [b])


def test_free_variables_1():
    a, b, c, d = make_variables("a b c d")
    ab = Application(
        of=a,
        on=b
    )
    c_ab = Abstraction(
        bound_variable=c,
        expression=ab
    )

    free_vars = find_free_variables(c_ab)
    assert_eq_iterable(free_vars, [a, b])


def test_free_variables_2():
    a, b, c, d = make_variables("a b c d")
    ab = Application(
        of=a,
        on=b
    )
    cab = Application(
        of=c,
        on=ab
    )

    d_cab = Abstraction(
        bound_variable=d,
        expression=cab
    )

    free_vars = find_free_variables(d_cab)
    assert_eq_iterable(free_vars, [c, a, b])


def test_free_variables_3():
    a, b, c, d = make_variables("a b c d")
    a_a = Abstraction(a, a)
    b_b = Abstraction(b, b)
    a_ab_b = Application(
        of=a_a,
        on=b_b
    )

    free_vars = find_free_variables(a_ab_b)
    assert_eq_iterable(free_vars, [])

    da_ab_b = Application(d, a_ab_b)
    free_vars = find_free_variables(da_ab_b)
    assert_eq_iterable(free_vars, [d])


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
