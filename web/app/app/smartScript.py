from app.tokenizer import Tokenizer
from app.parser import Parser
from app import interpreter
import time

hadError = False

def main(args = None):
    if args == None:
        while True:
            try:
                text = input('SmartScript> ')
            except EOFError:
                print('invalid')
                break
        
    code = args
    tokenizer = Tokenizer(code)
    tokens = tokenizer.getTokens()
    parser = Parser(tokens)
    statements = parser.parse()

    interpreter.Interpreter().interpret(statements)


def runtimeError(token, message):
    print(f'{token} {message}')
    hadError = True

