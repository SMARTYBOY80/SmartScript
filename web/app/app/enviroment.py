from app import tokens

class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.value in self.values:
            return self.values[name.value]
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(f"Undefined variable '{name.value}'.")
    
    def assign(self, name, value):
        if name.value in self.values:
            self.values[name.value] = value
            
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError(f"Undefined variable '{name.value}'.")