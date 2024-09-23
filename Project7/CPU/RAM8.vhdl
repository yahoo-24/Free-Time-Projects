library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity RAM8 is
	port (
		input   : in std_logic_vector(7 downto 0);
		output1  : out std_logic_vector(7 downto 0);
		output2 : out std_logic_vector(7 downto 0);
		address : in std_logic_vector(2 downto 0);
		load    : in std_ulogic;
		address1 : in std_logic_vector(2 downto 0);
		address2 : in std_logic_vector(2 downto 0);
		clk : in std_ulogic
 	);
end entity;


architecture behave of RAM8 is
	
	type mem is array (0 to 7) of std_logic_vector(7 downto 0);
	signal memory : mem  := ("00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000", "00000000");
	
begin
	
	output1 <= memory(to_integer(unsigned(address1)));
	output2 <= memory(to_integer(unsigned(address2)));
	
	pro1 : process (load, address, clk)
		variable i : integer;
	begin
		i := to_integer(unsigned(address));
		if load = '1' then
			memory(i) <= input;
		end if;
	end process;
end architecture;
