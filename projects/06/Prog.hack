address instruction: @i
command: M=1
address instruction: @sum
command: M=0
label: (LOOP)
address instruction: @i
command: D=M
address instruction: @100
command: D=D-A
address instruction: @END
command: D;JGT
address instruction: @i
command: D=M
address instruction: @sum
command: M=D+M
address instruction: @i
command: M=M+1
address instruction: @LOOP
command: 0;JMP
label: (END)
address instruction: @END
command: 0;JMP
