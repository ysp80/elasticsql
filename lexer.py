import ply.lex as lex

class Lexer(object):
  """docstring for Lexer"""
  def __init__(self):
    super(Lexer, self).__init__()
    #self.arg = arg
    self.num_count = 0
    self.build_rules()
    self.build()

  def build(self, **kwargs):
    self.lexer = lex.lex(object=self,**kwargs)

  def build_rules(self):
    self.reserved = {
       'AND' : 'AND',
       'OR' : 'OR'
    }

    self.tokens = [
       'NUMBER',
       'FIELD',
       'LPAREN',
       'RPAREN',
       'GTE',
       'LTE',
       'NE',
       'GT',
       'LT',
       'EQ'
    ] + list(self.reserved.values())

    self.t_LPAREN = r'\('
    self.t_RPAREN = r'\)'
    self.t_GTE = r'>='
    self.t_LTE = r'<='
    self.t_NE = r'!='
    self.t_GT = r'>'
    self.t_LT = r'<'
    self.t_EQ = r'='
    self.t_ignore = ' \t'

  def t_FIELD(self, t):
    r'[A-Za-z]+|[a-zA-Z_][a-zA-Z0-9_]*|[A-Z]*\.[A-Z]$'
    t.type = self.reserved.get(t.value,'FIELD')
    return t

  def t_NUMBER(self, t):
    r'\d+'
    t.value = int(t.value)
    return t

  def t_newline(self, t):
    r'\n+'
    t.lexer.lineno += len(t.value)

  def t_error(self, t):
    print("Illegal character '%s' " % t.value[0])
    t.lexer.skip(1)
    