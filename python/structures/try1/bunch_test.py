from bundle import Bunch


class DescribeBunch:
  def it_delegates_getattr(self):
    b = Bunch((1, 'a', []))

  def it_can_add(self):
    b = Bunch((1, 3, -2))
    assert Bunch.content(b.__add__.__call__(2)) == (3, 5, 0)
    assert Bunch.content(b + 2) == (3, 5, 0)

  def it_detects_inequality(self):
    assert Bunch.content(Bunch((1,)).__eq__(Bunch((2,)))) == (False,)

  def it_can_getitem(self):
    b = Bunch(([0, 1, 2], ('zero',), {0: 'blue'}))
    assert Bunch.content(b[0]) == (0, 'zero', 'blue')
