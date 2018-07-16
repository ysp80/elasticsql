from sqlyacc import Parser

class NodeVisitor(object):
  def visit(self, node):
    method_name = 'visit_' + type(node).__name__
    visitor = getattr(self, method_name, self.generic_visit)
    return visitor(node)

  def generic_visit(node):
    raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
  """docstring for Interpreter"""

  def __init__(self):
    self._parser = Parser()

  def translate(self, program):
    root = self._parser.parse(program)
    return self.visit(root)

  def visit_RootNode(self, node):
    output = '<Root>'
    for child in node.children:
      output += '\n' + self.visit(child)
    output += '</Root>'
    return output

  def visit_ComparisonNode(self, node):
    return '<Compare op="{0}" left="{1}" right="{2}" />'.format(node.op, node.left, node.right)

  def visit_LogicNode(self, node):
    output = '<Logic op="{0}" >'.format(node.op)
    for child in node.children:
      output += '\n' + self.visit(child)
    output += '</Logic>'
    return output

class ElasticInterpreter(Interpreter):
  def visit_RootNode(self, node):
    children_output = []
    for child in node.children:
      children_output.append(self.visit(child))

    print children_output
    output = {
      'query': {
        'constant_score': {}
      }
    }
    return output

  def visit_ComparisonNode(self, node):
    op_dict = {
      '>' : 'gt',
      '<' : 'lt',
      '>=': 'gte',
      '<=': 'lte',
      '=' : 'eq',
      '!=': 'ne',
    }
    op = op_dict[node.op]

    field = node.left
    value = node.right

    es_dsl = {}
    if op == 'eq':
      es_dsl = {
        'term': { field: value }
      }
    elif op in ['gte', 'lte', 'gt', 'lt']:
      es_dsl = {
        'range' : {
          field : {
            op : value
          }
        }
      }
    return es_dsl

  def visit_LogicNode(self, node):
    if node.op == 'AND':
      es_op = 'must'
    elif node.op == 'OR':
      es_op = 'should'

    output = {
      es_op : [self.visit(child) for child in node.children]
    }
    return output

    