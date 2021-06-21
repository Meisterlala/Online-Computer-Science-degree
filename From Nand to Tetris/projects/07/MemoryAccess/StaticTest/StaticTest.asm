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

	// pop static 8
	@SP
	AM=M-1
	D=M
	@StaticTest.8
	M=D

	// pop static 3
	@SP
	AM=M-1
	D=M
	@StaticTest.3
	M=D

	// pop static 1
	@SP
	AM=M-1
	D=M
	@StaticTest.1
	M=D

	// push static 3
	@StaticTest.3
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

	// push static 1
	@StaticTest.1
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

	// push static 8
	@StaticTest.8
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