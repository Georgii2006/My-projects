#This program differentiates given functions
#The program is able to find a derrivative:
#of a number (8)
#of a constant (7*x)
#of a varible which is raised to power (2*x^8)
#of a sum or a difference of functions (2*x+9*x^2)
#of a product of functions (x-7)*(2*x-8)
#of a quotient of function (x^2-7)/(x+8)
#of a complex expression (2*x^6-7)^3
#of basic trigonometric functions (sin(x), cos(x+8), (tan(x-8))^2, cot(2*x^2)^3)
#when using the function you should type 7*x instead of 7x
#when using the function you should type (cos(x))^2 instead of cos^2(x)
#when using the function you should type cos((x-2)^2) instead of cos(x)^2
#the previous rule applies to all trigonometric functions that can
#be recognised by the program

def dividing(expression):
    power = False
    common = '+', '-', '*', '/', '^', 'x'
    ignore_here = 0
    ignore_higher = 0
    l = []
    i = 0
    for symbol in expression:
        i += 1
        if symbol == '(':
            if power:
                ignore_higher+=1
                continue
            if not ignore_here:
                a, b = dividing(expression[i:])
                l.append(a)
                ignore_here += 1
                ignore_higher += 1
            else:
                ignore_here += 1
                ignore_higher += 1
                continue
        if symbol == ')':
            if ignore_here < 1:
                return l, ignore_higher
            ignore_here -= 1
            if power:
                ignore_higher += 1
                power = False
                continue
        if ignore_here:
            continue
        if symbol == '^':
            power = True
        if symbol in common:
            l.append(symbol)
        if symbol.isalpha():
            if expression[i-1:i+2] == 'cos':
                l.append('cos')
            if expression[i-1:i+2] == 'sin':
                l.append('sin')
            if expression[i-1:i+2] == 'tan':
                l.append('tan')
            if expression[i-1:i+2] == 'cot':
                l.append('cot')
        if symbol.isdigit():
            if len(l) > 0:
                if l[-1].isdigit():
                    l[-1] += symbol
                else:
                    l.append(symbol)
            else:
                l.append(symbol)
    return l, ignore_higher

def combining(l):
    expression = ''
    for item in l:
        if 'list' in str(type(item)):
            expression += '(' + combining(item) + ')'
            continue
        expression += item
    return expression

def derrivative(expression, l = []):
    if not l:
        print('original function: ', expression)
        l = dividing(expression)[0]
    if l[0] == '+':
        l = l[1:]
        return derrivative('', l)
    if l[0] == '-':
        list_of_minuses = []
        x = 0
        for x in range(len(l)):
            if l[x] == '+':
                return derrivative(l[x+1:]+l[:x])
        for x in range(len(l)):
            if l[x] == '-':
                l[x] = '+'
        return '-(' + derrivative('', l) + ')'
    if len(l) == 1:
        if 'list' in str(type(l[0])):
            return derrivative('', l[0])
        if l[0].isdigit():
            return '0'
        if l[0] == 'x':
            return '1'
    if '+' in l:
        i = l.index('+')
        return '(' + derrivative('', l[:i]) + '+' + derrivative('', l[i+1:]) + ')'
    if '-' in l:
        i = l.index('-')
        return '(' + derrivative('', l[:i]) + '+' + derrivative('', l[i+1:]) + ')'
    if '*' in l:
        i = l.index('*')
        return derrivative('', l[:i]) + '*' + combining(l[i+1:]) + '+' + combining(l[:i]) + '*' + derrivative('', l[i+1:])
    if '/' in l:
        i = l.index('/')
        return '(' + derrivative('', l[:i]) + '*' + combining(l[i+1:]) + '-' + combining(l[:i]) + '*' + derrivative('', l[i+1:]) + ')/(' + combining(l[i+1:]) + ')^2'
    if '^' in l:
        i = l.index('^')
        return derrivative('', l[i-1]) + '*' + l[i+1] + '*(' + combining(l[i-1]) + ')^' + str(int(l[i+1])-1)
    if 'cos' in l:
        i = l.index('cos')
        return '(' + derrivative('', l[i+1]) + ')' + '*(-sin(' + combining(l[i+1]) + '))'
    if 'sin' in l:
        i = l.index('sin')
        return '(' + derrivative('', l[i+1]) + ')' + '*(cos(' + combining(l[i+1]) + '))'
    if 'tan' in l:
        i = l.index('tan')
        return '(' + derrivative('', l[i+1]) + ')/(cos(' + combining(l[i+1]) + '))^2'
    if 'cot' in l:
        i = l.index('cot')
        return '(-' + derrivative('', l[i+1]) + ')/(sin(' + combining(l[i+1]) + '))^2'
    return ''


print(derrivative('8'))
print(derrivative('7*x'))
print(derrivative('2*x^8'))
print(derrivative('2*x+9*x^2'))
print(derrivative('(x-7)*(2*x-8)'))
print(derrivative('(x^2-7)/(x+8)'))
print(derrivative('(2*x^6-7)^3'))
print(derrivative('sin(x)'))
print(derrivative('cos(x+8)'))
print(derrivative('(tan(x-8))^2'))
print(derrivative('cos((x-8)^2)'))
print(derrivative('(x-8)^2'))
print(derrivative('(cot(2*x^2))^3'))
print(derrivative(('(2*x+8)^8')))
