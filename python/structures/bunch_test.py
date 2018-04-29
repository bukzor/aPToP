import decimal

import hypothesis as H
import hypothesis.strategies as st

from bunch import Bunch

hashables = st.one_of(
    st.booleans(),
    st.none(),
    st.integers(),
    st.tuples(st.deferred(lambda: hashables)),
    st.frozensets(st.deferred(lambda: hashables)),
    st.floats(),
    st.text(),
    st.binary(),
    st.fractions(),
    st.decimals().filter(lambda x: not decimal.Decimal.is_snan(x)),
    st.datetimes(),
    st.dates(),
    st.times(),
    st.timedeltas(),
    st.uuids()
)

all_things = st.one_of(
    hashables,
    st.one_of(
        st.lists(st.deferred(lambda: all_things)),
        st.sets(hashables),
        st.dictionaries(hashables, st.deferred(lambda: all_things)),
    ),
)

bunches = st.tuples(hashables).map(lambda x: Bunch(*x))


class DescribeBunch:
    def it_simple_containment(self):
        assert None in Bunch(None)
        assert 1 in Bunch(1, 2)
        assert frozenset(['x']) in Bunch(frozenset(['x']))

    def it_bunch_containment(self):
        assert Bunch(None) in Bunch(None)
        assert Bunch(1) in Bunch(1, 2)
        assert Bunch(frozenset(['x'])) in Bunch(frozenset(['x']))

    @H.given(hashables, bunches, bunches)
    def it_has_compound_axiom(self, x, A, B):
        assert (x in A + B) == (x in A or x in B)

    @H.given(bunches, bunches, bunches)
    def it_has_antidistrubivity(self, A, B, C):
        assert (A + B in C) == (A in C and B in C)

    @H.given(bunches, bunches, bunches)
    def it_has_distrubivity(self, A, B, C):
        assert (A in B * C) == (A in B and A in C)

    @H.given(bunches, bunches)
    def it_has_generalization(self, A, B):
        assert A in A + B

    @H.given(bunches, bunches)
    def it_has_specialization(self, A, B):
        assert A * B in A

    @H.given(bunches)
    def it_has_reflexivity(self, A):
        assert A in A

    @H.given(bunches, bunches)
    def it_has_antisymmetry(self, A, B):
        assert (A in B and B in A) == (A == B)

    @H.given(bunches, bunches)
    def it_has_antisymmetry(self, A, B):
        assert (A in B and B in A) == (A == B)

    @H.given(bunches, bunches, bunches)
    def it_has_transitivity(self, A, B, C):
        B = B + A
        C = C + B
        assert A in B and B in C
        assert A in C


class DescribeBunchUnion:
    @H.given(hashables)
    def it_has_idempotence(self, x):
        Bunch(x) + Bunch(x) == Bunch(x)

    @H.given(bunches, bunches)
    def it_has_symmetry(self, A, B):
        A + B == B + A

    @H.given(bunches, bunches, bunches)
    def it_has_associativity(self, A, B, C):
        assert A + (B + C) == (A + B) + C


class DescribeBunchIntersection:
    @H.given(hashables)
    def it_has_idempotence(self, x):
        Bunch(x) * Bunch(x) == Bunch(x)

    @H.given(bunches, bunches)
    def it_has_symmetry(self, A, B):
        A * B == B * A

    @H.given(bunches, bunches, bunches)
    def it_has_associativity(self, A, B, C):
        assert A * (B * C) == (A * B) * C


class DescribeBunchSize:
    @H.given(hashables)
    def it_is_one_when_elementary(self, x):
        len(Bunch(x)) == 1

    @H.given(bunches, bunches)
    def it_relates_to_intersection_and_union(self, A, B):
        len(A + B) + len(A * B) == len(A) + len(B)

    @H.given(hashables, bunches)
    def it_is_zero_on_disjoin_intersection(self, x, A):
        H.assume(x not in A)
        assert len(A * Bunch(x)) == 0

    @H.given(bunches, bunches)
    def it_is_smaller_for_subsets(self, A, B):
        B = A + B
        assert A in B
        assert len(A) <= len(B)
