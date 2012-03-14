"""Python Docs: A Python Documentation API for Developers

## Examples

** Parse a live Python object **
>>> import docs
>>> docs.get(docs)
<[Module] __init__>

** Parse file name**
>>> import docs as d
>>> m  = d.get(filename='docs/module/module.py')
>>> m
<[Module] module>
>>> m.docstring
'Wrapper object for Python modules'
"""
import ast
import inspect
import os
import sys

#from docs.classes import Class
#from docs.function import Function
from docs.imports import Import
from docs.visitors import Node
from docs.module import Module

__author__    = 'Michael Van Veen (michael@mvanveen.net)'
__copyright__ = 'Copyright 2012, Michael Van Veen'
__license__   = 'MIT'
__version__   = '0.1'
__email__     = "pythondocs@mvanveen.net"
__status__    = "Beta"

def get(*args, **kw):
  item = kw.get('item') or len(args) and args[0] or None
  path = kw.get('path')
  filename = kw.get('filename')

  if not len(args) and not (item or path or filename):
    return

  if isinstance(item, basestring):
    if item in sys.modules.keys():
      return get(path=item)
    try:
      return get(__import__(item))
    except ImportError:
      pass

  if isinstance(item, (Module, Import)):
    return item

  elif path:
    path = Import(Node(ast.parse('import %s' % (path, )).body[0]))
    return get(path._import)

  elif inspect.ismodule(item):
    file_str = item.__file__
    if file_str.endswith('.pyc'):
      file_str = file_str[:-1]
    return Module(filename=file_str)

  elif os.path.isdir(filename):
    return Module(filename=os.path.join(filename, '__init__.py'))

  elif filename:
    return Module(filename=filename)

  elif isinstance(item, ast.AST):
    if isinstance(item, ast.Import):
      return Import(item)
    return Node(item)

  elif isinstance(item, (list, tuple)):
    return [get(y) for y in item]

  #elif inspect.isclass(item):
  #  return Class(item)

  #elif inspect.isfunction(item):
  #  return Function(item):

  return item


def imports(*args, **kw):
  #TODO(mvv): add function and class
  node = get(*args, **kw)
  if isinstance(node, Module):
    return node.imports
  raise TypeError('must be Module, Function, or Class')
