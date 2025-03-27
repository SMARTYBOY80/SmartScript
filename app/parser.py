from enum import Enum
from app.tokens import Token, TokenType
from app import expressions, statements


class ParseError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def next(self):
        if self.isAtEnd():
          raise EOFError('End of file reached: no more tokens to parse')  
        return self.tokens[self.current + 1]

    def consume(self, type, message):
        if not self.check(type):
            self.error(self.peek(), message)
        return self.advance()


    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self, type):
        if self.isAtEnd():
            return False
        return self.peek().type == type

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()
    
    def isAtEnd(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def error(self, token, message):
        return ParseError(token, message)

    def expression(self): #starts a precendense chain of methods 
        '''
        expression     → equality ;
        equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        term           → factor ( ( "-" | "+" ) factor )* ;
        factor         → unary ( ( "/" | "*" ) unary )* ;
        unary          → ( "!" | "-" ) unary
                    | primary ;
        primary        → NUMBER | STRING | "true" | "false" | "nil"
                    | "(" expression ")" ;
        '''
        return self.assignment()
    

    def assignment(self):
        expr = self.Or()

        if self.match(TokenType.EQUAL):
            equals = self.previous()

            value = self.assignment()

            if isinstance(expr, expressions.Variable):
                name = expr.name
                return expressions.Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

    def Or(self):
        expr = self.And()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.And()
            expr = expressions.Logical(expr, operator, right)
        return expr
    
    def And(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = expressions.Logical(expr, operator, right)
        return expr

    def decleration(self):
        try:
            if self.match(TokenType.VAR): return self.varDecleration()
            if self.match(TokenType.FUN): return self.function("function")
            return self.statement()
        except ParseError as error:
            self.synchronize() 
            return None
    
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = expressions.Binary(expr, operator, right)
        return expr
    
    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = expressions.Binary(expr, operator, right)
        return expr
    
    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = expressions.Binary(expr, operator, right)
        return expr
    
    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR, TokenType.MODULO):
            operator = self.previous()
            right = self.unary()
            expr = expressions.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return expressions.Unary(operator, right)
        return self.call()
    
    def function(self, kind):
        name = self.consume(TokenType.ID, f"Expect {kind} name.")

        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")

        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(TokenType.ID, "Expect parameter name."))
            while self.match(TokenType.COMMA):
                if len(parameters) >= 127:
                    self.error(self.peek(), "Can't have more than 127 parameters.")
                parameters.append(self.consume(TokenType.ID, "Expect parameter name."))
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, "Expect '}' before body.")
        body = self.block()
        return statements.Function(name, parameters, body)
    
    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            else:
                break
        return expr
    
    def finishCall(self, callee):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(arguments) >= 127:
                    self.error(self.peek(), "Can't have more than 127 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")   
        return expressions.Call(callee, paren, arguments)

    def primary(self):
        if self.match(TokenType.FALSE):
            return expressions.Literal(False)
        if self.match(TokenType.TRUE):
            return expressions.Literal(True)
        if self.match(TokenType.NULL):
            return expressions.Literal(None)

        if self.match(TokenType.INTEGER, TokenType.FLOAT , TokenType.STRING):
            return expressions.Literal(self.previous().value)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expressions.Grouping(expr)
        
        if self.match(TokenType.ID):
            return expressions.Variable(self.previous())
        
        
        raise self.error(self.peek(), f"Expect expression. got {self.peek().type}")

    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in [TokenType.CLASS, TokenType.VAR, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.SORT, TokenType.RETURN]:
                return
            self.advance()

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        
        if self.match(TokenType.RANDOM):
            return self.random()

        if self.match(TokenType.SORT):
            return self.bubbleSort()
        if self.match(TokenType.LEFT_BRACE):
            return statements.Block(self.block())
        
        if self.match(TokenType.IF):
            return self.ifStatement()
        
        if self.match(TokenType.WHILE):
            return self.whileStatement()

        return self.expressionStatement()
    
    
    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after while condition.")
        body = self.statement()
        return statements.While(condition, body)
    
    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
        thenBranch = self.statement()
        elseBranch = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()
        return statements.If(condition, thenBranch, elseBranch)

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return statements.Print(value)
    
    def bubbleSort(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return statements.BubbleSort(value)
    
    def random(self):
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return statements.Random()
    
    def varDecleration(self):

        name = self.consume(TokenType.ID, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable decleration.")
        return statements.Var(name, initializer)
    
    def expressionStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return statements.Expression(value)
    
    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.decleration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
    
    def asignment(self):
        pass

    def binary(self):
        pass

    def addition(self):
        expr = self.multiplication()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.multiplication()
            expr = expressions.Binary(expr, operator, right)

        return expr



    def parse(self):
        stmts = []

        while not self.isAtEnd():
            stmts.append(self.decleration())

        return stmts