class Bunch(object):
  """A bunch is a bit like a tuple, but it automagically delegates operations
  to its contents, resulting in a new bundle."""
  __slots__ = ('__bunch__',)

  def __init__(self, *values):
    self.__bunch__ = frozenset(values)

  def __contains__(self, other):
    bunch = getattr(other, '__bunch__', None)
    if bunch is not None:
      return all(
        value in self
        for value in bunch
      )
    else:
      return other in self.__bunch__

  def __add__(self, other):
    cls = type(self)
    other = getattr(other, '__bunch__', 'other')
    return cls(*(self.__bunch__ | other))

  def __mul__(self, other):
    cls = type(self)
    other = getattr(other, '__bunch__', 'other')
    return cls(*(self.__bunch__ & other))

  def __eq__(self, other):
    cls = type(self)
    other = getattr(other, '__bunch__', 'other')
    return self.__bunch__ == other

  def __repr__(self):
    cls = type(self)
    return '%s%s' % (cls.__name__, tuple(self.__bunch__))

  def __len__(self):
    return self.__bunch__.__len__()
