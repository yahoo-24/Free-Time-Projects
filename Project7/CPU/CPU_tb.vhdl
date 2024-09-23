library IEEE;
use IEEE.std_logic_1164.all;

entity CPU_tb is
end entity;

architecture test of CPU_tb is

	signal status, clk : std_ulogic;
	signal CheckRAM, CheckALU, out1, out2, in1 : std_logic_vector(7 downto 0);
	
	component CPU
		port (
			status    : out std_ulogic;
			CheckRAM  : out std_logic_vector(7 downto 0);
			CheckALU  : out std_logic_vector(7 downto 0);
			clk       : in std_ulogic;
			out1      : out std_logic_vector(7 downto 0);
			out2      : out std_logic_vector(7 downto 0);
			in1       : out std_logic_vector(7 downto 0)
		);
	end component;
	
begin
	
	UUT : CPU port map (status => status, CheckRAM => CheckRAM, CheckALU => CheckALU, clk => clk, out1 => out1, out2 => out2, in1 => in1);

	clk_process: process
    begin
        while true loop
			clk <= '0';
			wait for 10 ns;
			clk <= '1';
			wait for 10 ns;
        end loop;
    end process;
	
	test_process: process
    begin
		
		wait for 140 ns;
		
        -- End simulation
        assert false report "Simulation Ended" severity failure;
    end process;
end test;