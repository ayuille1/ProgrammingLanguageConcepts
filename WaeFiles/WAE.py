from WAEParser import parser


def eval_expression(tree):
    if tree[0] == 'num':
        return tree[1]
    elif tree[0] == 'id':
        return 'ERROR'
    elif tree[0] == '+' or tree[0] == '-' or tree[0] == '*' or tree[0] == '/':
        v1 = eval_expression(tree[1])
        if v1 == 'ERROR':
            return 'ERROR'
        v2 = eval_expression(tree[2])
        if v2 == 'ERROR':
            return 'ERROR'
        if tree[0] == '+':
            return v1 + v2
        elif tree[0] == '-':
            return v1 - v2
        elif tree[0] == '*':
            return v1 * v2
        elif v2 != 0:
            return v1 / v2
        else:
            return 'ERROR'
    elif tree[0] == 'if':  # if clause
        v1 = eval_expression(tree[1])
        if v1 == 'ERROR':
            return 'ERROR'
        if v1 != 0:
            return eval_expression(tree[2])
        else:
            return eval_expression(tree[3])
    elif tree[0] == 'with': #with statement
        v2 = eval_expression(tree[2])
        if v2 == 'ERROR':
            return 'ERROR'
        if v2 != 0:
            v1 = tree[1]
            while tree[3][0] == 'withs':
                tree = eval_expression(tree[3])
            subbed = substitute_vars(v1, v2, tree[3])
            if subbed[0] == 'num':
               return eval_expression(subbed)
            else:
                return subbed
        if tree[3][0] == 'with' or tree[3][0] == 'withs':
            tree[3] = eval_expression(tree[3])

    else: #withs statement
        vars = tree[1]
        variables = []
        subbed = [0]
        while vars[0] == 'withs':
            v1 = vars[1]
            variables.append(v1)
            v2 = eval_expression(vars[2])
            if subbed[0] != 'num':
                while tree[2][0] == 'withs':
                    tree[2] = eval_expression(tree[2])
                subbed = substitute_vars(v1, v2, tree[2])
            if len(vars) >= 4:
                vars = vars[3]
            else:
                vars[0] = 0

        first_var_count = 0
        while first_var_count < len(variables):
            second_var_count = 0
            while second_var_count < len(variables):
                variable = variables[first_var_count]
                other_var = variables[second_var_count]
                if first_var_count != second_var_count:
                    if other_var == variable:
                        return 'ERROR'

                second_var_count += 1
            first_var_count += 1
        return eval_expression(subbed)


def substitute_vars(var, val, tree):
    if len(tree) >= 3:
        if tree[1][0] == 'withs':

            if tree[1] == ['id', var]:
                tree[1] = ['num', val]
            if tree[2] == ['id', var]:
                tree[2] = ['num', val]

        if tree[2][0] == '+' or tree[2][0] == '-' or tree[2][0] == '*' or tree[2][0] == '/':
            tree[2] = substitute_vars(var, val, tree[2])

        elif tree[1][0] == '+' or tree[1][0] == '-' or tree[1][0] == '*' or tree[1][0] == '/':
            tree[1] = substitute_vars(var, val, tree[1])

        if tree[2][0] == 'withs':
            eval_expression(tree[2])

        else:
            if tree[1][1] == var:
                tree[1] = ['num', val]
            if tree[2][1] == var:
                tree[2] = ['num', val]

        if tree[1][0] == 'num' and tree[2][0] == 'num':
            return ['num', eval_expression(tree)]
        else:
            return tree
    else:
        if tree[1] == var:
            tree = ['num', val]
            return tree


def read_input():
    result = ''
    while True:
        data = input('WAE: ').strip()
        if ';' in data:
            i = data.index(';')
            result += data[0:i + 1]
            break
        else:
            result += data + ' '
    return result


def main():
    while True:
        data = read_input()
        if data == 'exit;':
            break
        try:
            tree = parser.parse(data)
        except Exception as inst:
            print(inst.args[0])
            continue
        print(tree)
        try:
            answer = eval_expression(tree)
            print(answer)
            if answer == 'ERROR':
                print('\nEVALUATION ERROR\n')
            else:
                print('\nThe value is ' + str(answer) + '\n')
        except:
            pass


main()
