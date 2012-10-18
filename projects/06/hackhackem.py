#!/usr/bin/env python

# hackhackem.py - an assembler for Hack assembly language
# Hack is the architecure developed in the nand2tetris project
# author: nicolas steven miller

import sys

if len(sys.argv) != 2:
    print 'Usage: hasm input.asm'
    exit(-1)

try:
    assembly = open(sys.argv[1], 'r')
    binary = open(sys.argv[1].split('.')[0] + '.hack', 'w')
except IOError as e:
    print e.strerror + ': ' + e.filename
    exit(-1)


for line in assembly:
    # handle comments
    instruction = line.split('//')[0].strip()
    if len(instruction) == 0:
        continue

    output = ''
    if instruction[0] == '@':
        #if instruction[1:].isdigit():
            # write out value directly
        #else:
            # boo symbol
        output = 'address instruction: ' + instruction

    elif instruction[0] == '(':
        # create label in symbol tabel somehow
        output = 'label: ' + instruction
    else:
        # parse command
        output = 'command: ' + instruction
    binary.write(output + '\n')

assembly.close()
binary.flush()
binary.close()
    
