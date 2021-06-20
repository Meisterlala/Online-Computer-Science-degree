// Generated from projects/07/StackArithmetic/StackTest/StackTest.asm

	// push constant 17
	@17
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 17
	@17
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// eq
	@SP
	AM=M-1
	D=M
	A=A-1
	D=D-M
	@TRUE_00000009
	D;JEQ
	@SP
	A=M-1
	M=0
	@END_00000009
	0;JMP
(TRUE_00000009)
	@SP
	A=M-1
	M=-1
(END_00000009)

	// push constant 17
	@17
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 16
	@16
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// eq
	@SP
	AM=M-1
	D=M
	A=A-1
	D=D-M
	@TRUE_00000012
	D;JEQ
	@SP
	A=M-1
	M=0
	@END_00000012
	0;JMP
(TRUE_00000012)
	@SP
	A=M-1
	M=-1
(END_00000012)

	// push constant 16
	@16
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 17
	@17
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// eq
	@SP
	AM=M-1
	D=M
	A=A-1
	D=D-M
	@TRUE_00000015
	D;JEQ
	@SP
	A=M-1
	M=0
	@END_00000015
	0;JMP
(TRUE_00000015)
	@SP
	A=M-1
	M=-1
(END_00000015)

	// push constant 892
	@892
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 891
	@891
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
	@TRUE_00000018
	D;JGT
	@SP
	A=M-1
	M=0
	@END_00000018
	0;JMP
(TRUE_00000018)
	@SP
	A=M-1
	M=-1
(END_00000018)

	// push constant 891
	@891
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 892
	@892
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
	@TRUE_00000021
	D;JGT
	@SP
	A=M-1
	M=0
	@END_00000021
	0;JMP
(TRUE_00000021)
	@SP
	A=M-1
	M=-1
(END_00000021)

	// push constant 891
	@891
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 891
	@891
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
	@TRUE_00000024
	D;JGT
	@SP
	A=M-1
	M=0
	@END_00000024
	0;JMP
(TRUE_00000024)
	@SP
	A=M-1
	M=-1
(END_00000024)

	// push constant 32767
	@32767
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 32766
	@32766
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// gt
	@SP
	AM=M-1
	D=M
	A=A-1
	D=D-M
	@TRUE_00000027
	D;JLT
	@SP
	A=M-1
	M=0
	@END_00000027
	0;JMP
(TRUE_00000027)
	@SP
	A=M-1
	M=-1
(END_00000027)

	// push constant 32766
	@32766
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 32767
	@32767
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// gt
	@SP
	AM=M-1
	D=M
	A=A-1
	D=D-M
	@TRUE_00000030
	D;JLT
	@SP
	A=M-1
	M=0
	@END_00000030
	0;JMP
(TRUE_00000030)
	@SP
	A=M-1
	M=-1
(END_00000030)

	// push constant 32766
	@32766
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 32766
	@32766
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// gt
	@SP
	AM=M-1
	D=M
	A=A-1
	D=D-M
	@TRUE_00000033
	D;JLT
	@SP
	A=M-1
	M=0
	@END_00000033
	0;JMP
(TRUE_00000033)
	@SP
	A=M-1
	M=-1
(END_00000033)

	// push constant 57
	@57
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 31
	@31
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// push constant 53
	@53
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

	// push constant 112
	@112
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

	// neg
	@SP
	A=M-1
	D=0
	M=D-M

	// and
	@SP
	AM=M-1
	D=M
	A=A-1
	M=D&M

	// push constant 82
	@82
	D=A
	@SP
	A=M
	M=D
	@SP
	M=M+1

	// or
	@SP
	AM=M-1
	D=M
	A=A-1
	M=D|M

	// not
	@SP
	A=M-1
	M=!M