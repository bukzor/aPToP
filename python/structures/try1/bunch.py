class Bunch(object):
  """A bundle is a bit like a tuple, but it automagically delegates operations
  to its contents, resulting in a new bundle."""
  @classmethod
  def content(cls, bundle):
    return bundle.__content

  def __init__(self, content):
    if isinstance(content, Bunch):
      self.__content = tuple(content.__content)
    else:
      self.__content = tuple(content)

  def __getattr__(self, attr):
    cls = type(self)
    return cls(
      getattr(element, attr)
      for element in self.__content
    )

  @property
  def __add__(self):
    return self.__getattr__('__add__')

  @property
  def __radd__(self):
    return self.__getattr__('__radd__')

  def __eq__(self, other):
    if not isinstance(other, Bunch):
      return self.__getattr__('__eq__')(other)

    cls = type(self)
    return cls(
      x == y
      for x in self.__content
      for y in other.__content
    )

  def __call__(self, *args, **kwargs):
    cls = type(self)
    return cls(
      element(*args, **kwargs)
      for element in self.__content
    )

  def __getitem__(self, key):
    if not isinstance(key, Bunch):
      return self.__getattr__('__getitem__')(key)

    cls = type(self)
    return cls(
      x[y]
      for x in self.__content
      for y in key.__content
    )

  def __repr__(self):
    cls = type(self)
    return '%s(%s)' % (cls.__name__, self.__content)
