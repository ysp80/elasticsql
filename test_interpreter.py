from interpreter import Interpreter, ElasticInterpreter

def _main():
  # Test it out
  sql = '(universe = 1000 AND sharpe > 2) OR (turnover < 10 AND corr > 1)'

  i = ElasticInterpreter()
  output = i.translate(sql)
  print output

if __name__ == '__main__':
  _main()