library IEEE;
use IEEE.std_logic_1164.all;

entity Multiplier_tb is
end entity;

architecture test of Multiplier_tb is
	component Multiplier
		port (
			a : in std_logic_vector(3 downto 0);
			b : in std_logic_vector(3 downto 0);
			y : out std_logic_vector(7 downto 0)
		);
	end component;
	
	signal a, b : std_logic_vector(3 downto 0);
	signal y : std_logic_vector(7 downto 0);
	
begin
	UUT : Multiplier port map (a => a, b => b, y => y);
	
	process begin
		
		a <= "0110";
		b <= "0101";
		wait for 20 ns;
		
		a <= "1111";
		b <= "0011";
		wait for 20 ns;
		
		a <= "1111";
		b <= "1100";
		wait for 20 ns;
		
		a <= "0000";
		b <= "0110";
		wait for 20 ns;
		
		a <= "1010";
		b <= "1001";
		wait for 20 ns;
	
		assert false report "Test Ended!";
		wait;
	end process;
end test;