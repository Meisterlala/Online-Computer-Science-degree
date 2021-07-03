// Generated from projects\08\FunctionCalls\FibonacciElement\FibonacciElement.asm


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
	@9999
	@9999
	@0000000000000000
	@9999
	@9999

// function Main.fibonacci 0
(Main.fibonacci)
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

// push constant 2
	@2
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// lt                     
	@SP
	AM=M-1
	D=M
	A=A-1
	D=D-M
	@TRUE_0000000000000014
	D;JGT
	@SP
	A=M-1
	M=0
	@END_0000000000000014
	0;JMP
(TRUE_0000000000000014)
	@SP
	A=M-1
	M=-1
(END_0000000000000014)

// if-goto IF_TRUE
	@SP
	AM=M-1
	D=M
	@Main.fibonacci$IF_TRUE
	D;JNE

// goto IF_FALSE
	@Main.fibonacci$IF_FALSE
	0;JMP

// label IF_TRUE          
(Main.fibonacci$IF_TRUE)

// push argument 0        
	@ARG
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

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

// label IF_FALSE         
(Main.fibonacci$IF_FALSE)

// push argument 0
	@ARG
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// push constant 2
	@2
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// sub
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M-D

// call Main.fibonacci 1  
	@Main.fibonacci$ret.0
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
	@Main.fibonacci
	0;JMP
(Main.fibonacci$ret.0)
	@9999
	@9999
	@0000000000000024
	@9999
	@9999

// push argument 0
	@ARG
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

// push constant 1
	@1
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// sub
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M-D

// call Main.fibonacci 1  
	@Main.fibonacci$ret.1
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
	@Main.fibonacci
	0;JMP
(Main.fibonacci$ret.1)
	@9999
	@9999
	@0000000000000028
	@9999
	@9999

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

// function Sys.init 0
(Sys.init)
	@SP
	A=M
	@0
	D=A
	@SP
	M=M+D

// push constant 4
	@4
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

// call Main.fibonacci 1   
	@Main.fibonacci$ret.2
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
	@Main.fibonacci
	0;JMP
(Main.fibonacci$ret.2)
	@9999
	@9999
	@0000000000000043
	@9999
	@9999

// label WHILE
(Sys.init$WHILE)

// goto WHILE              
	@Sys.init$WHILE
	0;JMP