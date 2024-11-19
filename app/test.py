global source

global current
current = 0
source = ['!', '=']

def match(c, current):
    #if isAtEnd(): return False
    if source[current] != c: return False
    current += 1
    return True
c= source[current]
match c:
    case '!': print(match('=', current) and "BANG_EQUAL" or "BANG")
    