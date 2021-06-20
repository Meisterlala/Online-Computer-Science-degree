// Generated from projects/07/MemoryAccess/BasicTest/BasicTest.asm

	// push constant 10
	@10
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// pop local 0
	@1
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

	// push constant 21
	@21
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 22
	@22
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// pop argument 2
	@2
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

	// pop argument 1
	@2
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

	// push constant 36
	@36
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// pop this 6
	@3
	D=M
	@6
	D=D+A
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

	// push constant 42
	@42
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 45
	@45
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// pop that 5
	@4
	D=M
	@5
	D=D+A
	@13
	M=D
	@SP
	AM=M-1
	D=M
	@13
	A=M
	M=D

	// pop that 2
	@4
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

	// push constant 510
	@510
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// pop temp 6
	@SP
	AM=M-1
	D=M
	@11
	M=D

	// push local 0
	@1
	D=M
	@0
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

	// push that 5
	@4
	D=M
	@5
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

	// push argument 1
	@2
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

	// push this 6
	@3
	D=M
	@6
	A=D+A
	D=M
	@SP
	AM=M+1
	A=A-1
	M=D

	// push this 6
	@3
	D=M
	@6
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

	// sub
	@SP
	AM=M-1
	D=M
	A=A-1
	M=M-D

	// push temp 6
	@11
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