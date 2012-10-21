#!/usr/bin/env python

# vm_translator.py - implementation of the nand2tetris vm translator
# input: vm source file or directory containing vm source files
# output: equivalent hack assembly code

import sys
import os 

if len(sys.argv) != 2:
    print 'Usage: vm_translator.py input_file_or_dir'
    exit(-1)

path = os.path.split(sys.argv[1])[0]
head = os.path.split(sys.argv[1])[1]
output_filename = os.path.join(path, head.split('.')[0] + '.asm')

input_filenames = []
try:
    input_filenames = os.listdir(sys.argv[1])
except OSError:
    input_filenames.append(sys.argv[1])
input_filenames = filter(lambda filename: filename[-3:] == '.vm', 
                         input_filenames)

if len(input_filenames) == 0:
    print 'Input Error: expected .vm file or directory containing at least one'

addresses = {
    'stack': 256
}

op = {
    'add': '+', 
    'sub': '-', 
    'neg': '-', 
    'gt': 'gt', 
    'eq': 'eq',
    'lt': 'lt', 
    'and': '&', 
    'or': '|', 
    'not': '!'
}

class Parser:
    def __init__(self, filename):
        self.open_file(filename)

    def open_file(self, filename):
        try:
            vm_file = open(filename, 'r')
            self.lines = vm_file.readlines()
        except IOError as e:
            print e.strerror + ': ' + e.filename
            exit(-1)

        self.lines = filter(lambda l: len(l) > 0, 
                        map(lambda l: l.split('//')[0].strip(), 
                            self.lines))

    def has_more_commands(self):
        return len(self.lines) > 0 

    def advance(self):
        self.command = self.lines.pop(0)

    def command_type(self):
        cmd_type = {
            'pop': 'C_POP',
            'push': 'C_PUSH',
        }
        cmd = self.command.split()[0]    
        if op.has_key(cmd):
            return 'C_ARITHMETIC' 
        else:
            return cmd_type[cmd]
        
    def first_arg(self):
        if self.command_type() == 'C_ARITHMETIC':
            return self.command
        return self.command.split()[1]

    def second_arg(self):
        return self.command.split()[2]

class CodeWriter:
    def __init__(self, filename):
        self.open_file(filename)
        self.write_env_init()
        self.label_counter = -1 

    def open_file(self, filename):
        try:
            self.out = open(filename, 'w')
        except IOError as e:
            print e.strerror + ': ' + e.filename
            exit(-1)

    def write(self, inst):
        self.out.write(inst + '\n') 

    def write_env_init(self):
        # initialize stack pointer
        self.write('@256')
        self.write('D=A')
        self.write('@SP')
        self.write('M=D')

    def next_label(self):
        self.label_counter += 1
        return "label" + str(self.label_counter)

    def set_filename(self, filename):
        self.close()
        open_file(filename)

    def unary_op(self, op):
        return op == 'neg' or op == 'not'

    def logical_op(self, jump_type):
        true_label = self.next_label()
        end_label = self.next_label()
        self.write('D=D-M')
        self.write('@' + true_label)
        self.write('D;'+ jump_type)
        self.write('D=0')
        self.write('@' + end_label)
        self.write('0;JMP')
        self.write('(' + true_label + ')')
        self.write('D=-1')
        self.write('(' + end_label + ')')

    def write_arithmetic(self, command):
        if self.unary_op(command):
            # dec stack pointer
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')

            # push unary op result
            self.write('M=' + op[command] + 'M')
            
            self.write('@SP')
            self.write('M=M+1')
        else:
            # put the first argument in d
            self.write('@SP')
            self.write('A=M')
            self.write('A=A-1')
            self.write('A=A-1')
            self.write('D=M')

            # dec stack pointer
            self.write('@SP')
            self.write('M=M-1')

            # perform op - first arg in D, second pointed to by M
            self.write('A=M')

            if op[command] == 'eq':
                self.logical_op('JEQ') 
            elif op[command] == 'gt':
                self.logical_op('JGT') 
            elif op[command] == 'lt':
                self.logical_op('JLT') 
            else:
                self.write('D=D' + op[command] + 'M')

            # dec stack pointer
            self.write('@SP')
            self.write('M=M-1')

            # push result
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')

    def write_push_pop(self, command, segment, index): 
        if segment == 'constant':
            self.write('@' + str(index))
            self.write('D=A')
            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')

    def close(self):
        self.out.flush()
        self.out.close()

writer =  CodeWriter(output_filename)

for filename in input_filenames:
    parser = Parser(filename)
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == 'C_ARITHMETIC':
            writer.write_arithmetic(parser.first_arg())
        else:
            writer.write_push_pop(parser.command_type(),
                                 parser.first_arg(),
                                 parser.second_arg())
