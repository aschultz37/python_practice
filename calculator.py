'''This program calculates the result of an expression written in Reverse\
Polish Notation.
'''

intro_message = 'This program calculates expressions using Reverse Polish\
Notation.\n'
example = 'Ex.: 4 5 + 7 * 3 - 20 / 2 %\nUse \'clear\' to clear, \'quit\' to\
quit.\n'

print(intro_message)
print(example)

def get_expression():
    '''Gets expression from user input and returns it as a string.'''
    print('Pease enter the expression in Reverse Polish Notation (no\
    parentheses):')
    return input()

def parse_expression(expr):
    '''Parses an expression by spaces and returns it as a list.'''
    return expr.split(" ")


def do_operation(operator, operand, result):
    '''Performs an operation on two operands and returns result.\n
    If the operator is invalid, returns the second operand (result)\n
    unmodified.'''
    if operator == '+':
        return (float(result) + float(operand))
    elif operator == '-':
        return (float(result) - float(operand))
    elif operator == '*':
        return (float(result) * float(operand))
    elif operator == '/':
        return (float(result) / float(operand))
    elif operator == '%':
        return (float(result) % float(operand))
    else:
        print(f'Invalid operator: {operator}.\n')
        return result

def eval_expression(expr, running_result=0, continuing=False):
    '''Evaluates parsed RPN expression using a stack.\n
    If an error occurs, returns the running result.'''
    stack = []
    if continuing == True:
        stack.append(running_result)
    for i in expr:
        try:
            stack.append(int(i))
        except ValueError:
            try:
                stack.append(do_operation(i, stack.pop(), stack.pop()))
            except IndexError:
                print(f'Error in do_operation: Incorrect number of arguments.\
                 Check operator validity and operands.')
                return running_result
    try:
        return stack.pop()
    except IndexError:
        print(f'Error popping result: Empty list. Check operator validity and\
        operands.')
        return running_result

result = 0
cont = False

while True:
    expression = get_expression()
    if expression in ['quit', 'Quit', 'q', 'Q']:
        print('\nProgram closing.')
        break
    elif expression in ['clear', 'Clear', 'c', 'C', 'cl', 'Cl']:
        result = 0
        cont = False
        print('Cleared result.\n')
    else:
        parsed = parse_expression(expression)
        if(len(parsed) <= 1):
            print(f'Invalid input. Please try again.')
        else:
            if cont == False:
                result = eval_expression(parsed)
                cont = True
            else:
                result = eval_expression(parsed, result, cont)
                cont = True
        print(f'Result: {result:.5}\n')
