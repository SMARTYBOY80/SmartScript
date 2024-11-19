from tokenType import TokenType
from token import Token
from main import error

class Scanner:
    start = 0
    current = 0
    line = 1

    def __init__(self, source) -> None:
        self.source = source
        self.tokens = []

    keywords= {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)
    
    def advance(self) -> str:
        return self.source[self.current +1]

    def addToken(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def scanTokens(self):
        while self.isAtEnd() == False:
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens
    
    def match(self, expected):
        if self.isAtEnd():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]
    
    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]
    
    def isDigit(self, c):
        # not using isdigit() because of weird edge cases
        return c >= '0' and c <= '9'
    
    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
        
        while self.isDigit(self.peek()):
            self.advance()
        
        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))
        return


    def scanToken(self):
        char = self.advance()
        match char:
            case '(': self.addToken(TokenType.LEFT_PAREN)
            case ')': self.addToken(TokenType.RIGHT_PAREN)
            case '{': self.addToken(TokenType.LEFT_BRACE)
            case '}': self.addToken(TokenType.RIGHT_BRACE)
            case ',': self.addToken(TokenType.COMMA)
            case '.': self.addToken(TokenType.DOT)
            case '-': self.addToken(TokenType.MINUS)
            case '+': self.addToken(TokenType.PLUS)
            case ';': self.addToken(TokenType.SEMICOLON)
            case '*': self.addToken(TokenType.STAR)
            case '!': self.addToken(self.match('=') and TokenType.BANG_EQUAL or TokenType.BANG)
            case '=': self.addToken(self.match('=') and TokenType.EQUAL_EQUAL or TokenType.EQUAL)
            case '<': self.addToken(self.match('=') and TokenType.LESS_EQUAL or TokenType.LESS)
            case '>': self.addToken(self.match('=') and TokenType.GREATER_EQUAL or TokenType.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and self.isAtEnd() == False:
                        self.current += 1
                else:
                    self.addToken(TokenType.SLASH)
            case ' ', '\r', '\t': pass
            case '\n': self.line += 1
            case '"': self.string()
            case _:
                if self.isDigit(char):
                    self.number()
                elif self.isAlpha(char):
                    self.identifier()
                else:
                    error(self.line, "Unexpected character.")
                    
          
    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()

        text = self.source[self.start:self.current]
        type = self.keywords.get(text)
        if type == None:
            tyoe = TokenType.IDENTIFIER
        self.addToken(type)

    def isAlpha(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def string(self):
        while self.peek() != '"' and self.isAtEnd() == False:
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.isAtEnd():
            error(self.line, "Unterminated string.")
            return
        
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.addToken(TokenType.STRING, value)
        return