def calculate(calc, verbose = False):
    if check(calc):
        calc = calc_braces(calc, verbose)
        calc = calc_mult_div(calc, verbose)
        calc = calc_add_sub(calc, verbose)
        return calc
    else:
        print("Invalid input")
        return -1
        
def check(calc):
    braces_open = 0
    braces_close = 0
    allowed_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '(', ')', '.']

    for char in calc:
        if char not in allowed_chars:
            return False
        if char == '(':
            braces_open += 1
        if char == ')':
            braces_close += 1
            if braces_close > braces_open:
                return False
    
    return True

def calc_braces(calc, verbose):
    while '(' in calc:
        brace_depth = 0
        end_left = 0
        start_right = 0
        found_left = False
        start = True
        end = True

        for i in range(calc):
            if calc[i] == '(':
                if i != 0 and brace_depth == 0:
                    start = False
                brace_depth += 1
                if not found_left:
                    found_left = True
                    end_left = i
            if calc[i] == ')':
                brace_depth -= 1
                if brace_depth == 0:
                    if i != len(calc) - 1:
                        end = False
                    start_right = i + 1
                    break
        
        if not start:
            left = calc[:end_left]
            if left[-1] not in ['+', '-', '*', '/', '(']:
                left = left + '*'
        else:
            left = ''

        if not end:
            right = calc[start_right:]
            if right[0] not in ['+', '-', '*', '/', ')']:
                right = '*' + right
        else:
            right = ''


        mid = calc[end_left + 1:start_right - 1]
        mid = calculate(mid, verbose)
        
        calc = left + mid + right
        calc = replace_add_sub(calc)

        if verbose:
            print(f"Braces:   {calc}")
    
    return calc

def calc_mult_div(calc, verbose):
    while '*' in calc or '/' in calc:
        left_num = calc[0]
        right_num = ''
        operator = ''
        end_left = 0
        start_right = 0
        found_left = False
        start = True
        end = True
        negative = False

        for i in range(1, len(calc)):
            if negative:
                negative = False
                continue
            if calc[i] not in ['+', '-', '*', '/']:
                if not found_left:
                    left_num += calc[i]
                else:
                    right_num += calc[i]
            else:
                if found_left:
                    start_right = i
                    end = False
                    break
                elif calc[i] not in ['*', '/']:
                    left_num = ''
                    if calc[i + 1] == '-':
                        left_num += '-'
                        negative = True
                    end_left = i + 1
                    start = False
                else:
                    found_left = True
                    operator = calc[i]
                    if calc[i + 1] == '-':
                        right_num += '-'
                        negative = True

        left = calc[:end_left] if not start else ''
        right = calc[start_right:] if not end else ''

        mid = '{0:g}'.format(float(left_num) * float(right_num)) if operator == '*' else '{0:g}'.format(float(left_num) / float(right_num))
        
        calc = left + mid + right
        calc = replace_add_sub(calc)

        if verbose:
            print(f"Mult/Div: {calc}")
    
    return calc

def calc_add_sub(calc, verbose):
    while '+' in calc[1:] or '-' in calc[1:]:
        left_num = calc[0]
        right_num = ''
        operator = ''
        start_right = 0
        found_left = False
        end = True

        for i in range(1, len(calc)):
            if calc[i] not in ['+', '-']:
                if not found_left:
                    left_num += calc[i]
                else:
                    right_num += calc[i]
            else:
                if found_left:
                    start_right = i
                    end = False
                    break
                else:
                    found_left = True
                    operator = calc[i]

        right = calc[start_right:] if not end else ''

        left = '{0:g}'.format(float(left_num) + float(right_num)) if operator == '+' else '{0:g}'.format(float(left_num) - float(right_num))
        
        calc = left + right

        if verbose:
            print(f"Add/Sub:  {calc}")
    
    return calc

def replace_add_sub(calc):
    while '--' in calc or '+-' in calc or '-+' in calc:
        calc = calc.replace('--', '+')
        calc = calc.replace('+-', '-')
        calc = calc.replace('-+', '-')
    if calc[0] == '+':
        calc = calc[1:]
    return calc

calc = input("> ")
calc = ''.join(calc.split())
calculate(calc, verbose = True)