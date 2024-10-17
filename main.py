digits = [c for c in "01234567890."]
operators = [c for c in "+-*/()^"]


expression = input("Expression > ")


def split_tokens(exp):
    tokens = []
    current_token = ""
    for i in exp:
        if i in digits:
            current_token += i
        elif current_token:
            tokens.append(current_token)
            current_token = ""
        if i in operators:
            tokens.append(i)
    if current_token:
        tokens.append(current_token)
    return tokens

def eval_simple_expression(a, operator, b):
    match operator:
        case "*":
            return a * b
        case "/":
            return a / b
        case "^":
            return a ** b
        case "+":
            return a + b
        case "-":
            return a - b


def is_float(a):
    return isinstance(a, float) or (a.count(".") < 2 and ("".join(a[1:].split(".")).isdigit() if a[0] == "-" else "".join(a.split(".")).isdigit()))


def eval_exp_single_opp(tokens: list, ops):
    i = 0
    original_i = 0
    while i < len(tokens):
        if isinstance(tokens[i], str) and tokens[i] in ops:
            if not is_float(tokens[i-1]):
                return original_i-1
            if not is_float(tokens[i+1]):
                return original_i+1
            result = eval_simple_expression(float(tokens.pop(i-1)), tokens.pop(i-1), float(tokens.pop(i-1)))
            tokens.insert(i-1, result)
            i -= 3
            original_i += 2
        i += 1
        original_i += 1
    return -1


def show_error(tokens, index, message):
    print(" ".join(tokens))
    spacing_count = 0
    for i, v in enumerate(tokens):
        if index == i:
            break
        spacing_count += len(v) + (0 if i == 0 or i == len(tokens) - 1 else 1)
    print(" " * (spacing_count + 1) + "^"*len(tokens[index]))
    print(message)


def eval_exp(tokens: list):
    playground = tokens.copy()
    success = eval_exp_single_opp(playground, "^")
    if success != -1:
        show_error(tokens, success, "Invalid token for operation `^`.")
        return False
    success = eval_exp_single_opp(playground, "*/")
    if success != -1:
        show_error(tokens, success, "Invalid token for operation `*` or `/`.")
        return False
    success = eval_exp_single_opp(playground, "+-")
    if success != -1:
        show_error(tokens, success, "Invalid token for operation `+` or `-`")
        return False
    tokens.clear()
    tokens.extend(playground)
    return True


exp_tokens = split_tokens(expression)
if eval_exp(exp_tokens):
    print(exp_tokens[0])
