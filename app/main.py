import sys
from scanner import *
global hadError
hadError = False

def runFile(file: str):
    with open(file, "r") as f:
        source = f.read()
        run(source)

        if hadError:
            sys.exit(65)

def runPrompt():
    while True:
        source = input("> ")
        if source == "":
            break
        run(source)
        hadError = False

def run(source: str):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()

    for token in tokens:
        print(token)

def error(line: int, message: str):
    report(line, "", message)

def report(line: int, where: str, message: str):
    print(f"[line {line}] Error{where}: {message}")
    # im tempted to make this a useless error message
    # would be very funny 
    # [line who the fuck knows] Error: GoodLuck
    hadError = True


def main():
    if len(sys.argv) >1:
        print(f'usage: python3 main.py {sys.argv[0]}')
        sys.exit(64)
    elif len(sys.argv) == 1:
        runFile(sys.argv[0])
    else:
        runPrompt()

if __name__ == "__main__":
    main()
