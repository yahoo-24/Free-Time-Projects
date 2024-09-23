# CPU

## Description
This is an implementation of a CPU using and old version of VHDL (GHDL).

### Usage Instructions
There are several files included all of which are necessary for CPU.vhdl to run. A test bench CPU_tb is also included to test if the CPU works. The result is shown in CPU.vcd. In my case, I have used gtkwave to see the output of the .vcd file.
The instruction format is as follows:
- The first 3 bits determine the operation: 1. '011' load a value directly into the register, 2. '010' load a value into the register from the memory, 3. '100' store into the memory, 4. '001' is for arithmetic and logical operations.
- For 1, the next 13 bits should be '00' followed by the 8 bit value to be loaded, followed by a 3 bit value to indicate which register to store into.
- For 2, the next 13 bits '0000000' should be a 3 bit value of the memory location, followed by a 3 bit value to indicate which register to store into.
- For 3, the next 13 bits should be '0000000' a 3 bit value of the memory location to store into, followed by a 3 bit value to indicate which register to take the value from.
- For 4, the next 13 bits should be a 4 bit value of operation (see below), followed by three 3 bit values to indicate which register to store into, which 2 registers to take the values from for the operation respectively.

Operations:
- 0000 addition: a + b
- 0110 subtraction: a - b
- 0101 reverse subtraction: b - a
- 1000 AND: a AND b
- 1001 OR: a OR b
- 1010 bit clear: a AND NOT b
- 1100 XOR: a XOR b
- 1101 move: b
- 1111 invert: NOT b

## Technologies Used
- VHDL
