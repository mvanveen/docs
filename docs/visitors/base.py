import ast

from docs.visitors.function import FunctionVisitor
from docs.visitors._import import ImportVisitor
from docs.visitors.node import Node
from docs.visitors.query import QueryConstructor


class VisitorBase(FunctionVisitor, ImportVisitor, Node):
  def __init__(self, ast_node=None, source=None, *args, **kw):
    self._source  = source or None

    if not ast_node and self._source:
      ast_node = self._parsed

    elif ast_node:
      if isinstance(ast_node, Node):
        self._parsed = ast_node._ast_obj
      elif isinstance(ast_node, ast.AST):
        self._parsed = ast_node
      else:
        raise TypeError('ast_node must be an ast.AST or Node type!')

    else:
      raise TypeError('Need either source code or an ast object')

    if not isinstance(ast_node, Node):
        ast_node = Node(ast_node)

    super(FunctionVisitor, self).__init__(
      *([ast_node._ast_obj] + list(args)),
      **kw
    )


  def parse(self):
    """Returns parsed AST for a document
    """
    if not self._parsed:
      assert self._source
      self._parsed = ast.parse(self._source)

    return self._parsed


  @property
  def parsed(self):
    """Returns the parsed AST for a document (as a property)."""
    return self.parse()


  @property
  def source(self):
    """Source code of tree from the root node"""
    return self._source


  @property
  def docstring(self):
    """Returns the module-level docstring."""
    return ast.get_docstring(self.parsed)

