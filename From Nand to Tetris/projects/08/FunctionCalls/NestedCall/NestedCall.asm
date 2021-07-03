// Generated from projects\08\FunctionCalls\NestedCall\NestedCall.asm


// Bootstrap
	@256
	D=A
	@SP
	M=D
	@0
	D=A
	@LCL
	M=D-1
	@ARG
	M=D-1
	@THIS
	M=D-1
	@THAT
	M=D-1

// call Sys.init 0
	@Sys.init$ret.0
	D=A
	@SP
	AM=M+1
	A=A-1
	M=D
	@LCL
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@ARG
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@THIS
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@THAT
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@SP
	D=M
	@5
	D=D-A
	@ARG
	M=D
	@SP
	D=M
	@LCL
	M=D
	@Sys.init
	0;JMP
(Sys.init$ret.0)

// function Sys.init 0
(Sys.init)
	@SP
	A=M
	@0
	D=A
	@SP
	M=M+D

// push constant 4000	
	@4000
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop pointer 0
	@SP
	AM=M-1
	D=M
	@THIS
	M=D

// push constant 5000
	@5000
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop pointer 1
	@SP
	AM=M-1
	D=M
	@THAT
	M=D

// call Sys.main 0
	@Sys.main$ret.0
	D=A
	@SP
	AM=M+1
	A=A-1
	M=D
	@LCL
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@ARG
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@THIS
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@THAT
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@SP
	D=M
	@5
	D=D-A
	@ARG
	M=D
	@SP
	D=M
	@LCL
	M=D
	@Sys.main
	0;JMP
(Sys.main$ret.0)

// pop temp 1
	@SP
	AM=M-1
	D=M
	@6
	M=D

// label LOOP
(Sys.funcName$LOOP)

// goto LOOP
	@Sys.funcName$LOOP
	0;JMP

// function Sys.main 5
(Sys.main)
	@SP
	A=M
	M=0
	A=A+1
	M=0
	A=A+1
	M=0
	A=A+1
	M=0
	A=A+1
	M=0
	A=A+1
	@5
	D=A
	@SP
	M=M+D

// push constant 4001
	@4001
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop pointer 0
	@SP
	AM=M-1
	D=M
	@THIS
	M=D

// push constant 5001
	@5001
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop pointer 1
	@SP
	AM=M-1
	D=M
	@THAT
	M=D

// push constant 200
	@200
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop local 1
	@LCL
	D=M
	@1
	D=D+A
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

// push constant 40
	@40
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop local 2
	@LCL
	D=M
	@2
	D=D+A
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

// push constant 6
	@6
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop local 3
	@LCL
	D=M
	@3
	D=D+A
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

// push constant 123
	@123
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// call Sys.add12 1
	@Sys.add12$ret.0
	D=A
	@SP
	AM=M+1
	A=A-1
	M=D
	@LCL
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@ARG
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@THIS
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@THAT
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D
	@SP
	D=M
	@6
	D=D-A
	@ARG
	M=D
	@SP
	D=M
	@LCL
	M=D
	@Sys.add12
	0;JMP
(Sys.add12$ret.0)

// pop temp 0
	@SP
	AM=M-1
	D=M
	@5
	M=D

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

// push local 2
	@LCL
	D=M
	@2
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// push local 3
	@LCL
	D=M
	@3
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// push local 4
	@LCL
	D=M
	@4
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

// add
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M+D

// add
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M+D

// add
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M+D

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

// function Sys.add12 0
(Sys.add12)
	@SP
	A=M
	@0
	D=A
	@SP
	M=M+D

// push constant 4002
	@4002
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop pointer 0
	@SP
	AM=M-1
	D=M
	@THIS
	M=D

// push constant 5002
	@5002
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// pop pointer 1
	@SP
	AM=M-1
	D=M
	@THAT
	M=D

// push argument 0
	@ARG
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// push constant 12
	@12
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// add
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M+D

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