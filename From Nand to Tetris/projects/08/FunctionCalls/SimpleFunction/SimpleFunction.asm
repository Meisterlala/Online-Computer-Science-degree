// Generated from projects\08\FunctionCalls\SimpleFunction\SimpleFunction.asm


//Bootstrap

// function SimpleFunction.test 2
(SimpleFunction.test)
	@SP
	A=M
	M=0
	A=A+1
	M=0
	A=A+1
	@2
	D=A
	@SP
	M=M+D

// push local 0
	@LCL
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// push local 1
	@LCL
	D=M
	@1
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// add
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M+D

// not
	@SP
	A=M-1
	M=!M

// push argument 0
	@ARG
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// add
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M+D

// push argument 1
	@ARG
	D=M
	@1
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// sub
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M-D

// return
	@LCL
	D=M
	@14
	M=D
	@14
	D=M
	@5
	A=D-A
	D=M
	@15
	M=D
	@SP
	A=M-1
	D=M
	@ARG
	A=M
	M=D
	@ARG
	D=M+1
	@SP
	M=D
	@14
	D=M
	@1
	A=D-A
	D=M
	@THAT
	M=D
	@14
	D=M
	@2
	A=D-A
	D=M
	@THIS
	M=D
	@14
	D=M
	@3
	A=D-A
	D=M
	@ARG
	M=D
	@14
	D=M
	@4
	A=D-A
	D=M
	@LCL
	M=D
	@15
	A=M
	0;JMP