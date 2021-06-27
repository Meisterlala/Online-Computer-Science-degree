// Generated from projects/08/ProgramFlow/BasicLoop/BasicLoop.asm

	//Bootstrap

	// push constant 0    
	@0
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// pop local 0         
	@LCL
	D=M
	@0
	D=D+A
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

	// label LOOP_START
(BasicLoop.funcName$LOOP_START)

	// push argument 0    
	@ARG
	D=M
	@0
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

	// push local 0
	@LCL
	D=M
	@0
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

	// pop local 0	        
	@LCL
	D=M
	@0
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
	D=M
	@0
	A=D+A
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
	@0
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
	D=M
	@0
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

	// if-goto LOOP_START  
	@SP
	AM=M-1
	D=M
	@BasicLoop.funcName$LOOP_START
	D;JGT

	// push local 0
	@LCL
	D=M
	@0
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D