#program that uses the ply package to emulate a computer with infinite memory
#uses the basic instructions inc, dec, clr, jmp, and continue
#reads a file given as an argument and runs the code in the file
#the debug argument "-d" can also be given to see the program run line-by-line

from RAMParser import parser
import sys

def execute(registers, lines, labels, pc, pc_max, code):
    while True:
        if lines[pc]['opcode'] == 'inc':
            if len(sys.argv) == 3:
                print(f'Executing: {code[pc]}')
            if lines[pc]['register'] in registers:
                registers[lines[pc]['register']] += 1
            else:
                registers[lines[pc]['register']] = 1

        elif lines[pc]['opcode'] == 'dec':
            if len(sys.argv) == 3:
                print(f'Executing: {code[pc]}')
            if lines[pc]['register'] in registers:
                if registers[lines[pc]['register']] > 0:
                    registers[lines[pc]['register']] -= 1
                else:
                    registers[lines[pc]['register']] = 0

        elif lines[pc]['opcode'] == 'clr':
            if len(sys.argv) == 3:
                print(f'Executing: {code[pc]}')
            registers[lines[pc]['register']] = 0

        elif lines[pc]['opcode'] == 'mov':
            if len(sys.argv) == 3:
                print(f'Executing: {code[pc]}')
            if lines[pc]['register2'] in registers:
                registers[lines[pc]['register1']] = registers[lines[pc]['register2']]
            else:
                registers[lines[pc]['register1']] = 0

        elif lines[pc]['opcode'] == 'jmpa':
            if len(sys.argv) == 3:
                print(f'Executing: {code[pc]}')
            temp = pc
            length = len(lines[pc]['label_acc'])
            actual = lines[pc]['label_acc']
            access = actual[0:length - 1]
            if 'register' in lines[pc]:
                if lines[pc]['register'] not in registers:
                    registers[lines[pc]['register']] = 0
                if registers[lines[pc]['register']] == 0:
                    while temp >= 0:
                        if temp in labels:
                            if labels[temp] == access:
                                pc = temp
                                break
                        temp -= 1
                    continue
                if temp < 0:
                    print(f'Error at line {pc}. Label {actual} not found below line {pc}.')
                    return 'ERROR'
            else:
                while temp >= 0:
                    if temp in labels:
                        if labels[temp] == access:
                            pc = temp
                            break
                    temp -= 1
                continue

        elif lines[pc]['opcode'] == 'jmpb':
            if len(sys.argv) == 3:
                print(f'Executing: {code[pc]}')
            temp = pc
            length = len(lines[pc]['label_acc'])
            actual = lines[pc]['label_acc']
            access = actual[0:length - 1]
            if 'register' in lines[pc]:
                if lines[pc]['register'] not in registers:
                    registers[lines[pc]['register']] = 0
                if registers[lines[pc]['register']] == 0:
                    while temp <= pc_max:
                        if temp in labels:
                            if labels[temp] == access:
                                pc = temp
                                break
                        temp += 1
                    continue
                if temp > pc_max:
                    print(f'Error at line {pc}. Label {actual} not found below line {pc}.')
                    return 'ERROR'
            else:
                while temp <= pc_max:
                    if temp in labels:
                        if labels[temp] == access:
                            pc = temp
                            break
                    temp += 1
                continue

        elif lines[pc]['opcode'] == 'CONTINUE':
            if len(sys.argv) == 3:
                print(f'Executing: {code[pc]}')
            if 'R1' in registers:
                return registers['R1']
            else:
                return 0

        pc += 1



def label(lines, pc):
    labels = {}
    for instr in lines:
        if 'label' in instr:
            labels[pc] = instr['label']
            lines[pc] = instr['code']
        pc += 1
    return labels


def store(lines):
    code = []
    string = ''
    for dict in lines:
        if 'label' in dict:
            string += dict['label'] + '    '
            dict = dict['code']
        if dict['opcode'] == 'inc' or dict['opcode'] == 'dec' or dict['opcode'] == 'clr':
            string += dict['opcode'].upper() + ' '
            string += dict['register']

        elif dict['opcode'] == 'mov':
            string += dict['opcode'].upper() + ' '
            string += dict['register1'] + ', '
            string += dict['register2']

        elif dict['opcode'] == 'jmpa' or dict['opcode'] == 'jmpb':
            if 'register' in dict:
                string += dict['register'] + ' '
            string += dict['opcode'].upper() + ' '
            string += dict['label_acc']

        elif dict['opcode'] == 'CONTINUE':
            string += dict['opcode'].upper()

        code.append(string)
        string = ''
    return code


def read_program():
    try:
        arglen = len(sys.argv)
        if arglen == 2:
            f = open(sys.argv[1], "r")
        elif arglen == 3:
            f = open(sys.argv[2], "r")
        file = f.read()
        tree = parser.parse(file)
        return tree
    except:
        print('File does not exist')
        return -1


def main():
    pc = 0
    print('Input:')
    data = read_program()
    if data == -1:
        print('Please try again with a file that exists.')
    elif data == -2:
        print('Please only supply arguments "RAM.py -d file" or "RAM.py file"')
    else:
        registers = data[0]
        for key in registers:
            print(f'{key} ==> {registers[key]}')
        lines = data[1]
        code = store(lines)
        labels = label(lines, pc)
        pc_max = len(lines)-1
        pc = 0
        result = execute(registers, lines, labels, pc, pc_max, code)
        print()
        print('Output: ')
        print(f'R1 = {result}')
main()
