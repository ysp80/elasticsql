import ply.yacc as yacc
from lexer import Lexer

class Node(object):
  def __init__(self, type, children = None, leaf = None):
    self.type = type
    if children:
      self.children = children
    else:
      self.children = []
    self.leaf = leaf

class RootNode(Node):
  def __init__(self, **kwargs):
    kwargs['type'] = 'logic'
    super(RootNode, self).__init__(**kwargs)

class ComparisonNode(Node):
  def __init__(self, left, op, right):
    self.type = "comparison"
    self.left = left
    self.right = right
    self.op = op

class LogicNode(Node):
  def __init__(self, op, **kwargs):
    kwargs['type'] = 'logic'
    super(LogicNode, self).__init__(**kwargs)
    self.op = op

class Parser(object):
  """docstring for Parser"""
  def __init__(self):
    super(Parser, self).__init__()
    #self.arg = arg
    lexer = Lexer()
    self.tokens = lexer.tokens
    self.build()

  def parse(self, program):
    rootNode = RootNode()
    rootNode.children.append(self._parser.parse(program))
    return rootNode

  def p_expression_term(self, p):
    'expression : boolean_term'
    p[0] = p[1]

  def p_expression_or(self, p):
    'expression : expression OR boolean_term'
    p[0] = LogicNode(op = p[2], children = [p[1], p[3]])

  def p_boolean_term_factor(self, p):
    'boolean_term : boolean_factor'
    p[0] = p[1]

  def p_boolean_term_and(self, p):
    'boolean_term : boolean_term AND boolean_factor'
    p[0] = LogicNode(op = p[2], children = [p[1], p[3]])

  def p_boolean_factor_comparison(self, p):
    'boolean_factor : field comparison_op value'
    p[0] = ComparisonNode(op = p[2], left = p[1], right= p[3])

  def p_comparison_op(self, p):
    '''comparison_op : EQ
                      | NE
                      | LT
                      | LTE
                      | GT
                      | GTE '''
    p[0] = p[1]

  def p_boolean_factor_expr(self, p):
    'boolean_factor : LPAREN expression RPAREN'
    p[0] = p[2]

  def p_field_name(self, p):
    'field : FIELD'
    p[0] = p[1]

  def p_value_num(self, p):
    'value : NUMBER'
    p[0] = p[1]

  def p_error(self, p):
    print('Syntax error')

  def build(self, **kwargs):
    self._parser = yacc.yacc(module=self, **kwargs)