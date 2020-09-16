// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// res = 0
// for i=0;i!=R0;i++
//     res = res + R1
//  R2 = res


@R2
M=0 // res=0

@i
M=0 // i = 0

(Loop)

@i
D=M
@R0
D=D-M
@end
D;JEQ // if i-R0==0 goto end


@R1
D=M
@R2
M=M+D   // res=res+R1

@i
M=M+1   // i++

@Loop
0;JMP

(end)
@end
0;JMP


