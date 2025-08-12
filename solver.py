from sympy import Eq, solve, simplify
from sympy.parsing.latex import parse_latex

def processMath(latex):
  if '=' in latex:#we have an equation
    left_str, right_str = latex.split("=")
    left_expr = parse_latex(left_str)
    right_expr = parse_latex(right_str)
    equation = Eq(left_expr, right_expr)

    return {
      "type": "equation", 
      "solutions": solve(equation)
      }
  else:#we have an expression
    expr = parse_latex(latex)

    return {
      "type": "expression",
      "simplified": simplify(expr)
    }