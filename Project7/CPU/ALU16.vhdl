library ieee;
use ieee.std_logic_1164.all;

entity mux is
	port (
		a : in std_logic_vector(7 downto 0);
		sel_1 : in std_ulogic;
		out1 : out std_logic_vector(7 downto 0)
	);
end entity;

architecture behaviour of mux is
begin
	out1 <= a when sel_1 = '0' else not a;
end behaviour;



library ieee;
use ieee.std_logic_1164.all;

entity lu is
	port (
		a : in std_logic_vector(7 downto 0);
		b : in std_logic_vector(7 downto 0);
		sel_1 : in std_ulogic;
		sel_2 : in std_ulogic;
		out_lu : out std_logic_vector(7 downto 0)
	);
end entity;

architecture behaviour of lu is
begin
	process(a, b, sel_1, sel_2)
	begin
		if (sel_1 = '0' and sel_2 = '0') then
			out_lu <= a and b;
		elsif (sel_1 = '1' and sel_2 = '0') then
			out_lu <= a or b;
		elsif (sel_1 = '0' and sel_2 = '1') then
			out_lu <= a xor b;
		else
			out_lu <= b;
		end if;
	end process;
end behaviour;


library ieee;
use ieee.std_logic_1164.all;

entity full is
	port (
		a : in std_ulogic;
		b : in std_ulogic;
		cin : in std_ulogic;
		cout : out std_ulogic;
		sum : out std_ulogic
	);
end entity;

architecture behaviour of full is
begin
	sum <= a xor b xor cin;
	cout <= ((a xor b) and cin) or (a and b);
end behaviour;


library ieee;
use ieee.std_logic_1164.all;

entity au is
	port (
		a : in std_logic_vector(7 downto 0);
		b : in std_logic_vector(7 downto 0);
		cin : in std_ulogic;
		v : out std_ulogic;
		c : out std_ulogic;
		out_au : out std_logic_vector(7 downto 0)
	);
end entity;

architecture behaviour of au is
	signal c1, c2, c3, c4, c5, c6, c7, c8 : std_ulogic;
	
	component full
		port (
			a : in std_ulogic;
			b : in std_ulogic;
			cin : in std_ulogic;
			cout : out std_ulogic;
			sum : out std_ulogic
		);
	end component;
begin
	U1 : full port map (a => a(0), b => b(0), cin => cin, sum => out_au(0), cout => c1);
	U2 : full port map (a => a(1), b => b(1), cin => c1, sum => out_au(1), cout => c2);
	U3 : full port map (a => a(2), b => b(2), cin => c2, sum => out_au(2), cout => c3);
	U4 : full port map (a => a(3), b => b(3), cin => c3, sum => out_au(3), cout => c4);
	U5 : full port map (a => a(4), b => b(4), cin => c4, sum => out_au(4), cout => c5);
	U6 : full port map (a => a(5), b => b(5), cin => c5, sum => out_au(5), cout => c6);
	U7 : full port map (a => a(6), b => b(6), cin => c6, sum => out_au(6), cout => c7);
	U8 : full port map (a => a(7), b => b(7), cin => c7, sum => out_au(7), cout => c8);
	c <= c8;
	v <= c8 xor c7;
end behaviour;


library ieee;
use ieee.std_logic_1164.all;

entity mux2 is
    port (
        in1  : in std_logic_vector(7 downto 0);
        in2  : in std_logic_vector(7 downto 0);
        sel  : in std_ulogic;
        out1 : out std_logic_vector(7 downto 0)
    );
end entity;

architecture behaviour of mux2 is
begin
    out1 <= in1 when sel='0' else in2;
end behaviour;



library ieee;
use ieee.std_logic_1164.all;

entity ALU16 is
	port (
		a      : in std_logic_vector(7 downto 0);
		b      : in std_logic_vector(7 downto 0);
		opcode : in std_logic_vector(3 downto 0);
		V      : out std_ulogic;
		N      : out std_ulogic;
		Z      : out std_ulogic;
		C      : out std_ulogic;
		result : out std_logic_vector(7 downto 0)
	);
end entity;

architecture behaviour of ALU16 is
	signal muxa, muxb, result_au, result_lu, resultx : std_logic_vector(7 downto 0);

	component au
		port (
			a : in std_logic_vector(7 downto 0);
			b : in std_logic_vector(7 downto 0);
			cin : in std_ulogic;
			v : out std_ulogic;
			c : out std_ulogic;
			out_au : out std_logic_vector(7 downto 0)
		);
	end component;
	
	component lu
		port (
			a : in std_logic_vector(7 downto 0);
			b : in std_logic_vector(7 downto 0);
			sel_1 : in std_ulogic;
			sel_2 : in std_ulogic;
			out_lu : out std_logic_vector(7 downto 0)
		);
	end component;
	
	component mux
		port (
			a : in std_logic_vector(7 downto 0);
			sel_1 : in std_ulogic;
			out1 : out std_logic_vector(7 downto 0)
		);
	end component;
	
	component mux2
        port (
            in1  : in std_logic_vector(7 downto 0);
            in2  : in std_logic_vector(7 downto 0);
            sel  : in std_ulogic;
            out1 : out std_logic_vector(7 downto 0)
        );
    end component;
	
begin
	U1 : mux port map (a => b, sel_1 => opcode(1), out1 => muxb);
	U2 : mux port map (a => a, sel_1 => opcode(0), out1 => muxa);
	U3 : au port map (a => muxa, b => muxb, cin => opcode(2), v => V, c => C, out_au => result_au);
	U4 : lu port map (a => a, b => muxb, sel_1 => opcode(0), sel_2 => opcode(2), out_lu => result_lu);
	U5 : mux2 port map (in1 => result_au, in2 => result_lu, sel => opcode(3), out1 => resultx);
	Z <= not(result_au(0) or result_au(1) or result_au(2) or result_au(3) or result_au(4) or result_au(5) or result_au(6) or result_au(7));
	N <= resultx(7);
	result <= resultx;
end behaviour;