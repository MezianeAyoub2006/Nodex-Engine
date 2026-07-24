from ..expression import Expression

class FExpressionNode(Expression):
    def __init__(self, f, *args, **kwargs):
        super().__init__()
        self.args = args 
        self.kwargs = kwargs 
        self.f = f 

    def resolve(self, target):
        return self.f(target, *self.args, **self.kwargs) 

    def __repr__(self):
        return f"{self.f.__name__}()" 
      
def f(func, *args, **kwargs):
    return FExpressionNode(func, *args, **kwargs)