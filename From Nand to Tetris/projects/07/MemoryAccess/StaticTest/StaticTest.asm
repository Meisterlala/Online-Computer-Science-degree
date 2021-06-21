// Generated from projects/07/MemoryAccess/StaticTest/StaticTest.asm

	// push constant 111
	@111
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 333
	@333
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 888
	@888
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

	// add
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M+D