class Token():
    def __init__(self, type, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __str__(self):
        return f'Token: {self.token}, Token Type: {self.token_type}'