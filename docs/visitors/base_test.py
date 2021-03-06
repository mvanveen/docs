import ast
import inspect
import unittest

from docs.visitors.base import VisitorBase, NoSourceCodeError
from docs.visitors.node import Node


def test_can_construct_base():
  a = ast.parse(inspect.getsource(ast))
  assert VisitorBase(a)


def test_can_construct_base_with_node():
  n = Node(ast.parse(inspect.getsource(ast)))
  assert VisitorBase(n)


def test_can_construct_base_with_source():
    v = VisitorBase(source=inspect.getsource(ast))
    assert v


class VisitorBaseTest(unittest.TestCase):

  def setUp(self):
    self.a = ast.parse(inspect.getsource(ast))
    self.v = VisitorBase(self.a)


  def test_can_get_imports(self):
    assert len(self.v.imports) == 4, 'Expected 4 imports in ast module!'


  def test_can_get_imports(self):
    num_funs = 10
    assert len(self.v.functions) == num_funs, \
      'Espected %s function defs in AST module!' % (num_funs, )


  def test_can_get_docstring(self):
    assert self.v.docstring.split('\n')[0] == 'ast'


  def test_cannot_get_source(self):
    self.failUnlessRaises(NoSourceCodeError, getattr, self.v, 'source')


  def test_can_get_source(self):
    v = VisitorBase(source=inspect.getsource(ast))
    assert v.source.split('\n')[0] == '# -*- coding: utf-8 -*-'


  def test_can_get_classes(self):
    assert len(self.v.classes) == 2, 'Expected 2 classes in ast module!'


  def test_can_filter_function_name(self):
    assert [x for x in self.v.functions if x.name == 'parse']

