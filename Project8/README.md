# Multiplier

## Description
This is an implementation of a multiplier using and old version of VHDL (GHDL). In this implementation I also include the implementation of a carry-look-ahead adder. The multiplier multiplies two 4 bit values and and generates a 7 bit output.

### Usage Instructions
A test bench Multiplier_tb.vhdl is also included to test if the multiplier works. The result is shown in Multiplier.vcd. In my case, I have used gtkwave to see the output of the .vcd file. You can adjust the values in the test bench to test for different 4 bit values of a and b and run in the comand prompt:
  ```bash
  ghdl -a Multiplier.vhdl
  ghdl -a Multiplier_tb.vhdl
  ghdl -e Multiplier_tb
  ghdl -r Multiplier_tb --vcd=Multiplier.vcd
  ```
This would generate the required vcd file.

## Technologies Used
- VHDL
