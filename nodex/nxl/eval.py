from .expression import Expression
from .entry import Entry
from .operator import ACTIONS

def evaluate(target, expression: Expression):
    if expression is None:
        return True  
    
    if isinstance(expression, (int, float, str, bool)):
        return expression 
    
    elif isinstance(expression, Entry):
        return ACTIONS[expression.op](
            evaluate(target, expression.left),  
            evaluate(target, expression.right) 
        )
    
    elif hasattr(expression, "resolve"):
        if expression.target:
            return expression.resolve(expression.target)
        else:
            return expression.resolve(target)
    
