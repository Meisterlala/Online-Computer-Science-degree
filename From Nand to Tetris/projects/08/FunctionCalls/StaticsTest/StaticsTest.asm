// Generated from projects\08\FunctionCalls\StaticsTest\StaticsTest.asm


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

// function Class1.set 0
(Class1.set)
	@SP
	A=M
	@0
	D=A
	@SP
	M=M+D

// push argument 0
	@ARG
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// pop static 0
	@SP
	AM=M-1
	D=M
	@Class1.0
	M=D

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

// pop static 1
	@SP
	AM=M-1
	D=M
	@Class1.1
	M=D

// push constant 0
	@0
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

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

// function Class1.get 0
(Class1.get)
	@SP
	A=M
	@0
	D=A
	@SP
	M=M+D

// push static 0
	@Class1.0
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// push static 1
	@Class1.1
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

// function Class2.set 0
(Class2.set)
	@SP
	A=M
	@0
	D=A
	@SP
	M=M+D

// push argument 0
	@ARG
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// pop static 0
	@SP
	AM=M-1
	D=M
	@Class2.0
	M=D

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

// pop static 1
	@SP
	AM=M-1
	D=M
	@Class2.1
	M=D

// push constant 0
	@0
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

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

// function Class2.get 0
(Class2.get)
	@SP
	A=M
	@0
	D=A
	@SP
	M=M+D

// push static 0
	@Class2.0
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// push static 1
	@Class2.1
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

// function Sys.init 0
(Sys.init)
	@SP
	A=M
	@0
	D=A
	@SP
	M=M+D

// push constant 6
	@6
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

// call Class1.set 2
	@Class1.set$ret.0
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
	@7
	D=D-A
	@ARG
	M=D
	@SP
	D=M
	@LCL
	M=D
	@Class1.set
	0;JMP
(Class1.set$ret.0)

// pop temp 0 
	@SP
	AM=M-1
	D=M
	@5
	M=D

// push constant 23
	@23
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// push constant 15
	@15
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// call Class2.set 2
	@Class2.set$ret.0
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
	@7
	D=D-A
	@ARG
	M=D
	@SP
	D=M
	@LCL
	M=D
	@Class2.set
	0;JMP
(Class2.set$ret.0)

// pop temp 0 
	@SP
	AM=M-1
	D=M
	@5
	M=D

// call Class1.get 0
	@Class1.get$ret.0
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
	@Class1.get
	0;JMP
(Class1.get$ret.0)

// call Class2.get 0
	@Class2.get$ret.0
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
	@Class2.get
	0;JMP
(Class2.get$ret.0)

// label WHILE
(Sys.init$WHILE)

// goto WHILE
	@Sys.init$WHILE
	0;JMP