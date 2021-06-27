// Generated from projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.asm

	//Bootstrap

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

	// pop pointer 1           
	@SP
	AM=M-1
	D=M
	@THAT
	M=D

	// push constant 0
	@0
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// pop that 0              
	@THAT
	D=M
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

	// push constant 1
	@1
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// pop that 1              
	@THAT
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

	// pop argument 0          
	@ARG
	D=M
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

	// label MAIN_LOOP_START
(FibonacciSeries.funcName$MAIN_LOOP_START)

	// push argument 0
	@ARG
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

	// if-goto COMPUTE_ELEMENT 
	@SP
	AM=M-1
	D=M
	@FibonacciSeries.funcName$COMPUTE_ELEMENT
	D;JGT

	// goto END_PROGRAM        
	@FibonacciSeries.funcName$END_PROGRAM
	0;JMP

	// label COMPUTE_ELEMENT
(FibonacciSeries.funcName$COMPUTE_ELEMENT)

	// push that 0
	@THAT
	A=M
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

	// push that 1
	@THAT
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

	// pop that 2              
	@THAT
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

	// push pointer 1
	@THAT
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

	// add
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M+D

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

	// pop argument 0          
	@ARG
	D=M
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

	// goto MAIN_LOOP_START
	@FibonacciSeries.funcName$MAIN_LOOP_START
	0;JMP

	// label END_PROGRAM
(FibonacciSeries.funcName$END_PROGRAM)