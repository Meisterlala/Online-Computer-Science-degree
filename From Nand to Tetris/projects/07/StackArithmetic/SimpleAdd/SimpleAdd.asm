// Generated from projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm
// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@SP
M=M-1