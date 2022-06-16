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

    ab = Application(of=a, on=b)
    cab = Application(of=c, on=ab)
    cab = Application(of=cab, on=d)

    Abstraction(bound_variable=d, expression=cab)


def test_free_variables_0():
    a, b, c, d = make_variables("a b c d")
    assert_eq_iterable(find_free_variables(a), [a])

    ab = Application(a, b)
    assert_eq_iterable(find_free_variables(ab), [a, b])

    a_b = Abstraction(a, b)
    assert_eq_iterable(find_free_variables(a_b), [b])


def test_free_variables_1():
    a, b, c, d = make_variables("a b c d")
    ab = Application(of=a, on=b)
    c_ab = Abstraction(bound_variable=c, expression=ab)

    free_vars = find_free_variables(c_ab)
    assert_eq_iterable(free_vars, [a, b])


def test_free_variables_2():
    a, b, c, d = make_variables("a b c d")
    ab = Application(of=a, on=b)
    cab = Application(of=c, on=ab)

    d_cab = Abstraction(bound_variable=d, expression=cab)

    free_vars = find_free_variables(d_cab)
    assert_eq_iterable(free_vars, [c, a, b])


def test_free_variables_3():
    a, b, c, d = make_variables("a b c d")
    a_a = Abstraction(a, a)
    b_b = Abstraction(b, b)
    a_ab_b = Application(of=a_a, on=b_b)

    free_vars = find_free_variables(a_ab_b)
    assert_eq_iterable(free_vars, [])

    da_ab_b = Application(d, a_ab_b)
    free_vars = find_free_variables(da_ab_b)
    assert_eq_iterable(free_vars, [d])


def test_basic_substitution():
    a, b, c = make_variables("a b c")

    a__substituted = substitution(a, a, b)
    assert isinstance(a__substituted, Variable)
    assert a__substituted == b

    ab = Application(a, b)
    ab__substituted = substitution(ab, b, c)
    assert isinstance(ab__substituted, Application)
    assert ab__substituted.of == a
    assert ab__substituted.on == c

    a_b = Abstraction(a, b)
    a_b__substituted = substitution(a_b, a, c)
    assert isinstance(a_b__substituted, Abstraction)
    assert isinstance(a_b__substituted.expression, Variable)
    assert a_b__substituted.bound_variable == a
    assert a_b__substituted.on == c



