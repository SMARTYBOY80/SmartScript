from app import expressions
from app.tokens import TokenType
from app import statements
from app.enviroment import Environment
import time
import random




class Callable:
    def call(self, interpreter, arguments):
        pass

    def arity(self):
        pass

class Function:
    def __init__(self, name, params, body) -> None:
        self.name = name
        self.params = params
        self.body = body

    def bind(self, instance):
        Environment = Environment(self.closure)
        Environment.define("this", instance)
        return Function(self.name, self.params, self.body, Environment)

    def arity(self):
        return len(self.params)
    
    def __repr__(self) -> str:
        return f"<fn {self.name}>"

    def call(self, interpreter, arguments):
        Environment = Environment(interpreter.globals)
        for i in range(len(self.params)):
            Environment.define(self.params[i].value, arguments[i])
        interpreter.execute_block(self.body, Environment)

class Interpreter():

    def __init__(self) -> None:
        self.globals = Environment()
        self.environment = self.globals
        self.defClock()


    def defClock(self):
        
        def clock(*args):
            return time.time
        
        self.globals.define("clock", clock)

    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)
    
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
    
    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
    
    def evaluate(self, expr):
        return expr.accept(self)
    

    def execute(self, stmt):
        stmt.accept(self)

    def is_number(self, obj) -> bool:
        return isinstance(obj, (int, float))
    
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.operator.type == TokenType.MINUS:
            return left - right
        elif expr.operator.type == TokenType.PLUS:
            if (self.is_number(left) and self.is_number(right)) or (isinstance(left, str) and isinstance(right, str)):
                return left + right
            raise RuntimeError("Operands must be two numbers or two strings")
        if expr.operator.type == TokenType.SLASH:
            return left / right
        elif expr.operator.type == TokenType.STAR:
            return left * right
        elif expr.operator.type == TokenType.MODULO:
            return left % right 
        elif expr.operator.type == TokenType.GREATER:
            return left > right
        elif expr.operator.type == TokenType.GREATER_EQUAL:
            return left >= right
        elif expr.operator.type == TokenType.LESS:
            return left < right
        elif expr.operator.type == TokenType.LESS_EQUAL:
            return left <= right
        elif expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        elif expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)


        # Unreachable
        return "how the fuck did you get here"       

    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.token_type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -right
        elif expr.operator.token_type == TokenType.BANG:
            return not self.is_trueish(right)
        
        # Unreachable
        return "how the fuck did you get here"
    
    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    
    def is_trueish(self, obj):
        if obj == None: return False
        if isinstance(obj, bool): return obj

    def is_equal(self, left, right):
        if left == None and right == None: return True
        if left == None: return False
        return (left == right)
    
    def stringify(self, obj):
        if obj == None: return 'null'

        if isinstance(obj, float):
            obj = str(obj)
            if obj.endswith(".0"):
                obj =obj[:2]
            return obj
        return str(obj)
    

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))

    def visit_bubble_sort_stmt(self, stmt):
        # Bubble sort 
        text = self.evaluate(stmt.expression)
        
        array = text.split(",")
        for i in range(len(array)):
            swapped = False

            for j in range(0, len(array) - i - 1):

                if array[j] > array[j + 1]:

                    temp = array[j]
                    array[j] = array[j+1]
                    array[j+1] = temp

                    swapped = True
            if not swapped:
                break

        print(array)

    def visit_var_stmt(self, stmt):
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        else:
            value = None
        self.environment.define(stmt.name.value, value)

    def visit_random_stmt(self, stmt):
        # Random number generator
        rando = random.randint(0, 100)
        print(rando)

    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)

        return None
    
    def visit_function_stmt(self, stmt):
        function = Function(stmt.name, stmt.params, stmt.body)
        self.environment.define(stmt.name.value, function)
        return None

    def visit_if_stmt(self, stmt):
        if self.is_trueish(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.is_trueish(left):
                return left
        else:
            if not self.is_trueish(left):
                return left

        return self.evaluate(expr.right)
    
    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = [self.evaluate(arg) for arg in expr.arguments]

        if not isinstance(callee, Callable):
            raise RuntimeError("Can only call functions and classes.")

        if len(arguments) != callee.arity():
            raise RuntimeError(f"Expected {callee.arity()} arguments but got {len(arguments)}.")
        print(callee.call(self, arguments))
        return callee.call(self, arguments)

    def visit_while_stmt(self, stmt):
        while self.is_trueish(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def interpret(self, stmts) -> None:
        for stmt in stmts:
            self.execute(stmt)
