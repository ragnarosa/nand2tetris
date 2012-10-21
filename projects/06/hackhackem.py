#!/usr/bin/env python

# hackhackem.py - an assembler for Hack assembly language
# (Hack is the architecure developed in the nand2tetris project)
# yes the project specifies that ascii '0's and '1's be written out...
#
# author: nicolas steven miller

import sys
import os

if len(sys.argv) != 2:
    print 'Usage: hackhackem.py input.asm'
    exit(-1)

path = os.path.split(sys.argv[1])[0]
head = os.path.split(sys.argv[1])[1]
output_filename = os.path.join(path, head.split('.')[0] + '.hack')

try:
    assembly = open(sys.argv[1], 'r')
    binary = open(output_filename, 'w')
except IOError as e:
    print e.strerror + ': ' + e.filename
    exit(-1)

symbol_table = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576
}

comp = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001101',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
}

dest = {
    '': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}

jump = {
    '': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

current_rom_address = 0
current_data_address = 16

def is_valid(symbol):
    return (not symbol[0].isdigit() and 
            all(map(lambda s: s.isalpha or s.isdigit or s in '_.$:', symbol)))   

def is_variable(statement):
    return statement[0] == '@' and is_valid(statement[1:])

def identifier(variable_statement):
    return variable_statement[1:] 

def label(label_statement):
    return label_statement[1:-1]

def is_label(statement):
    return statement[0] == '(' and statement[-1] == ')' and is_valid(statement[1:])

# first pass -- add labels to symbol table
for line in assembly:
    # ignore comments and white space
    statement = line.split('//')[0].strip()
    if len(statement) == 0:
        continue

    if is_label(statement):
        symbol_table[label(statement)] = current_rom_address
        continue
    
    current_rom_address += 1

assembly.seek(0)

for line in assembly:
    # ignore comments and white space
    statement = line.split('//')[0].strip()
    if len(statement) == 0:
        continue

    output = ''
    if statement[0] == '@':
        address = current_data_address
        if is_variable(statement):
            try: 
                address = symbol_table[identifier(statement)]
            except KeyError:
                symbol_table[identifier(statement)] = current_data_address
                current_data_address += 1 
        else:
            try:
                address = int(identifier(statement))
            except ValueError:
                print 'Invalid @address instruction'
                exit(-1)
        output = bin(address)[2:]
        output = '0' * (16 - len(output)) + output
        assert len(output) == 16
    elif statement[0] == '(':
        continue
    else:
        output = '111'
        statement = statement.split('=')
        if len(statement) == 1:
            statement = statement[0].split(';')
            statement = map(lambda s: s.strip(), statement)
            assert len(statement) == 2
            output += comp[statement[0]] + '000' + jump[statement[1]]
        else:
            statement = map(lambda s: s.strip(), statement)
            assert len(statement) == 2
            output += comp[statement[1]] + dest[statement[0]] + '000'
    binary.write(output + '\n')

assembly.close()
binary.flush()
binary.close()
