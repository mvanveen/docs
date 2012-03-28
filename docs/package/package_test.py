import unittest

import docs
from docs.package import Package
from docs.modules import Module

def test_cosntruct_package():
  assert Package(filename='docs/'), 'Could not successfully construct package'


class PackageTest(unittest.TestCase):
  def setUp(self, *args, **kw):
    self._pak = Package(filename='docs/')


  def test_get_packages(self):
    assert Package('docs/classes') in self._pak.packages, \
      "Expected docs/classes to be in packages attribute"


  def test_get_modules(self):
    assert docs.get(path='docs') in self._pak.modules, \
      "Expected docs __init__.py file to be in modules attribute"


  def test_get_imports(self):
    import os
    assert os in [x._import for x in self._pak.imports]


  def test_get_docstring(self):
    assert self._pak.docstring == \
      'Python Docs: A Python Documentation API for Developers'


  def test_get_functions(self):
    mod = Module(filename='docs/__init__.py')
    assert [x.name == y.name for x, y in zip(mod.functions, self._pak.functions)]
