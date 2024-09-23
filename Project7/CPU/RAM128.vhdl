library IEEE;
use IEEE.std_logic_1164.all;

entity dlatch2 is
	port (
		d : in std_ulogic;
		e : in std_ulogic;
		q : out std_ulogic
	);
end dlatch2;

architecture behave of dlatch2 is
begin
	process (e)
	begin
	
	if e = '0' then
		q <= d;
	end if;
	end process;
end behave;



library IEEE;
use IEEE.std_logic_1164.all;

entity dff2 is
	port (
		d   : in std_ulogic;
		clk : in std_ulogic;
		clr : in std_ulogic;
		q   : out std_ulogic
		);
end dff2;


architecture behave of dff2 is
	signal q1, clk_temp, q2 : std_ulogic;
	
	component dlatch2
		port (
			d : in std_ulogic;
			e : in std_ulogic;
			q : out std_ulogic
		);
	end component;
	
begin
	clk_temp <= not clk;
	Master : dlatch2
		port map (
			d => d,
			e => clk_temp,
			q => q1
		);
	Slave : dlatch2
		port map (
			d => q1,
			e => clk,
			q => q2
		);
	q <= q2 and clr;
end behave;


library IEEE;
use IEEE.std_logic_1164.all;

entity bit_reg is
	generic (
		clr : std_logic := '1'
	);
	port (
		inp  : in std_ulogic;
		load : in std_ulogic;
		outp : out std_ulogic
	);
end bit_reg;

architecture behave of bit_reg is
	component dff2
		port (
			d   : in std_ulogic;
			clk : in std_ulogic;
			clr : in std_ulogic;
			q   : out std_ulogic
		);
	end component;
	
begin
	reg : dff2 port map (d => inp, clk => load, clr => clr, q => outp);
end behave;



library IEEE;
use IEEE.std_logic_1164.all;

entity reg8 is
	port (
		load : in std_ulogic;
		inp  : in std_logic_vector(7 downto 0);
		outp : out std_logic_vector(7 downto 0)
	);
end entity;


architecture behave of reg8 is
	component bit_reg
		port (
			inp  : in std_ulogic;
			load : in std_ulogic;
			outp : out std_ulogic
		);
	end component;
	
begin
	gen_reg : for i in 0 to 7 generate
		register8 : bit_reg port map (inp => inp(i), outp => outp(i), load => load);
	end generate;
end behave;



library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity RAM128 is
	port (
		input   : in std_logic_vector(7 downto 0);
		output  : out std_logic_vector(7 downto 0);
		address : in std_logic_vector(2 downto 0);
		load    : in std_ulogic;
		clk     : in std_ulogic
 	);
end entity;


architecture behave of RAM128 is
	
	type mem is array (0 to 7) of std_logic_vector(7 downto 0);
	signal memory : mem  := ("00000000", "00000000", "00000000", "00000000",
	"00000000", "00000000", "00000000", "00000000");
	
begin
	pro1 : process (load, address, clk)
		variable i : integer;
	begin
		i := to_integer(unsigned(address));
		if load = '1' then
			memory(i) <= input;
		else
			output <= memory(i);
		end if;
	end process;
end architecture;

	--gen_ram : for i in 0 to 7 generate
		--ram : reg16 port map (inp => input((15+16*i) downto 16*i), outp => outp(i), load => load);
	--end generate;
	