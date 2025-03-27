'''
 _________  ________  ___  __    _______   ________   ___  ________  _______   ________     
|\___   ___\\   __  \|\  \|\  \ |\  ___ \ |\   ___  \|\  \|\_____  \|\  ___ \ |\   __  \    
\|___ \  \_\ \  \|\  \ \  \/  /|\ \   __/|\ \  \\ \  \ \  \\|___/  /\ \   __/|\ \  \|\  \   
     \ \  \ \ \  \\\  \ \   ___  \ \  \_|/_\ \  \\ \  \ \  \   /  / /\ \  \_|/_\ \   _  _\  
      \ \  \ \ \  \\\  \ \  \\ \  \ \  \_|\ \ \  \\ \  \ \  \ /  /_/__\ \  \_|\ \ \  \\  \| 
       \ \__\ \ \_______\ \__\\ \__\ \_______\ \__\\ \__\ \__\\________\ \_______\ \__\\ _\ 
        \|__|  \|_______|\|__| \|__|\|_______|\|__| \|__|\|__|\|_______|\|_______|\|__|\|__|

'''

from app.tokens import Token, TokenType

def error(text):
    raise ValueError(text)

RESERVED_KEYWORDS = {
    'and': "AND",
    'class': "CLASS",
    'else': "ELSE",
    'false': "FALSE",
    'fun': "FUN",
    'for': "FOR",
    'if': "IF",
    'null': "NULL",
    'or': "OR",
    'print': "PRINT",
    'SORT': "SORT",
    'return': "RETURN",
    'super': "SUPER",
    'this': "THIS",
    'true': "TRUE",
    'var': "VAR",
    'while': "WHILE"
}

class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0
        self.current_char = self.code[self.pos]
        self.linenum = 1

    def getTokens(self) -> list:
        while self.pos in range(len(self.code)):
            self.tokenize()
        self.tokens.append(Token(TokenType.EOF, 'EOF', self.linenum, self.pos))
        return self.tokens
    

    def advance(self) -> None:
        self.pos += 1
        if self.pos > len(self.code) - 1:
            self.current_char = None
        else:
            self.current_char = self.code[self.pos]

    def peek(self) -> str:
        peek_pos = self.pos + 1
        if peek_pos > len(self.code) - 1:
            return ""
        else:
            return self.code[peek_pos]
        
    def skip_whitespace(self) -> None:
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.linenum += 1
            self.advance()

    def skip_comment(self) -> None:
        while self.current_char != '|':
            self.advance()
        self.advance()

    def number(self) -> Token:
        number = ''
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        
        if self.current_char == '.':
            number += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                number += self.current_char
                self.advance()
            return Token(TokenType.FLOAT, float(number), self.linenum, self.pos)

        return Token(TokenType.INTEGER, int(number), self.linenum, self.pos)
    
    def id(self) -> Token:
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        if result in RESERVED_KEYWORDS:
            return Token(TokenType(result.upper()), result, self.linenum, self.pos)
        return Token(TokenType.ID, result, self.linenum, self.pos)
    

    def tokenize(self) -> list:
        self.current_char = self.code[self.pos]
        match self.current_char:
            case None:
                pass
            case ' ':
                self.skip_whitespace()
            case '"':
                self.advance()
                string = ''
                while self.current_char is not None and self.current_char != '"':
                    string += self.current_char
                    self.advance()
                self.advance()
                self.tokens.append( Token(TokenType.STRING, string, self.linenum, self.pos))
            case '\n':
                self.advance()
                self.linenum += 1
            case '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    self.tokens.append( Token(TokenType.EQUAL_EQUAL, '==', self.linenum, self.pos))
                else:
                    self.tokens.append( Token(TokenType.EQUAL, '=', self.linenum, self.pos))
            case '+':
                self.advance()
                self.tokens.append( Token(TokenType.PLUS, '+', self.linenum, self.pos))
            case '-':
                self.advance()
                self.tokens.append( Token(TokenType.MINUS, '-', self.linenum, self.pos))
            case '*':
                self.advance()
                self.tokens.append( Token(TokenType.STAR, '*', self.linenum, self.pos))
            case '%':
                self.advance()
                self.tokens.append( Token(TokenType.MODULO, '%', self.linenum, self.pos))
            case '/':
                self.advance()
                if self.current_char == '/':
                    self.advance()
                    self.skip_comment()
                else:
                    self.tokens.append( Token(TokenType.SLASH, '/', self.linenum, self.pos))
            case '(':
                self.advance()
                self.tokens.append( Token(TokenType.LEFT_PAREN, '(', self.linenum, self.pos))
            case ')':
                self.advance()
                self.tokens.append( Token(TokenType.RIGHT_PAREN, ')', self.linenum, self.pos))
            case ';':
                self.advance()
                self.tokens.append( Token(TokenType.SEMICOLON, ';', self.linenum, self.pos))
            case '.':
                self.advance()
                self.tokens.append( Token(TokenType.DOT, '.', self.linenum, self.pos))
            case ',':
                self.advance()
                self.tokens.append( Token(TokenType.COMMA, ',', self.linenum, self.pos))
            case '{':
                self.advance()
                self.tokens.append( Token(TokenType.LEFT_BRACE, '{', self.linenum, self.pos))
            case '}':
                self.advance()
                self.tokens.append( Token(TokenType.RIGHT_BRACE, '}', self.linenum, self.pos))
            case '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    self.tokens.append( Token(TokenType.BANG_EQUAL, '!=', self.linenum, self.pos))
                else:
                    self.tokens.append( Token(TokenType.BANG, '!', self.linenum, self.pos))

            case '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    self.tokens.append( Token(TokenType.GREATER_EQUAL, '>=', self.linenum, self.pos))
                else:
                    self.tokens.append( Token(TokenType.GREATER, '>', self.linenum, self.pos))

            case '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    self.tokens.append( Token(TokenType.LESS_EQUAL, '<=', self.linenum, self.pos))
                else:
                    self.tokens.append( Token(TokenType.LESS, '<', self.linenum, self.pos))
                    
            case _ if self.current_char.isdigit():
                self.tokens.append( self.number())
            case _ if self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append( self.id())
            case _:
                error(f"Invalid character '{self.current_char}'")

  