// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

(RESET_SCREEN_COUNTER)
    @8192
    D=A
    @SCREEN_COUNTER
    M=D

(RESET_MASK_COUNTER)
    @16
    D=A
    @MASK_COUNTER
    M=D

(RESET_MASK)
    @1
    D=A
    @MASK
    M=D

@SCREEN_COUNTER
MD=M-1
@RESET_SCREEN_COUNTER
D;JLT


(IO_LOOP)
    @24576
    D=M
    @CLEAR
    D;JEQ
    @FILL
    D;JNE
 
(CLEAR)
    @SCREEN
    D=A
    @SCREEN_COUNTER
    D=D+M
    @TEMP
    M=D
    @MASK
    D=!M
    @TEMP
    A=M
    M=D&M
    @ITER
    0;JMP

(FILL)
    @SCREEN
    D=A
    @SCREEN_COUNTER
    D=D+M
    @TEMP
    M=D
    @MASK
    D=M
    @TEMP
    A=M
    M=D|M

(ITER)
    @MASK_COUNTER
    MD=M-1
    @RESET_MASK_COUNTER
    D;JEQ

    @MASK
    D=M
    M=D+M
    @IO_LOOP
    0;JMP
