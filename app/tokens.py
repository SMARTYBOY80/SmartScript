from enum import Enum
class Token:
    def __init__(self, type, value, linenum, column):
        self.type = type        #TokenType
        self.value = value      #str
        self.linenum = linenum  #int
        self.column = column    #int

    def __str__(self) -> str:
        return f'Token({self.type}, {self.value})'
    
    def __repr__(self) -> str:
        return self.__str__()

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN          =   '('
    RIGHT_PAREN         =   ')'
    LEFT_BRACE          =   '{'
    RIGHT_BRACE         =   '}'
    COMMA               =   ','
    DOT                 =   '.'
    MINUS               =   '-'
    PLUS                =   '+'
    SEMICOLON           =   ';'
    SLASH               =   '/'
    STAR                =   '*'

  # One or two character tokens.
    BANG                =   '!'
    BANG_EQUAL          =   '!='
    EQUAL               =   '='
    EQUAL_EQUAL         =   '=='
    GREATER             =   '>'
    GREATER_EQUAL       =   '>='
    LESS                =   '<'
    LESS_EQUAL          =   '<='
    MODULO              =   '%'

  # Literals.
    ID                  =   'ID'
    STRING              =   'STRING'  
    INTEGER             =   'INTEGER'
    FLOAT               =   'FLOAT'


  # Keywords.
    AND                 =   'AND'
    CLASS               =   'CLASS'
    ELSE                =   'ELSE'
    FALSE               =   'FALSE'
    FUN                 =   'FUN'
    FOR                 =   'FOR'
    IF                  =   'IF'
    RANDOM              =   'RANDOM'
    NULL                =   'NULL'
    OR                  =   'OR'
    PRINT               =   'PRINT'
    SORT                =   'SORT'
    RETURN              =   'RETURN'
    SUPER               =   'SUPER'
    THIS                =   'THIS'
    TRUE                =   'TRUE'
    VAR                 =   'VAR'   
    WHILE               =   'WHILE'


  # End of file
    EOF                 =   'EOF'


