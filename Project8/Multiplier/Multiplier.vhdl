library IEEE;
use IEEE.std_logic_1164.all;

entity Adder is
	port (
		a      : in std_logic_vector(3 downto 0);
		b      : in std_logic_vector(3 downto 0);
		output : out std_logic_vector(3 downto 0);
		cin    : in std_ulogic;
		cout   : out std_ulogic
	);
end entity;

architecture behaviour of Adder is
begin
	process (a, b, cin)
		variable c1, c2, c3: std_ulogic;
		variable p0, p1, p2, p3 : std_ulogic;
		variable g0, g1, g2, g3 : std_ulogic;
	begin
		p0 := a(0) xor b(0);
		p1 := a(1) xor b(1);
		p2 := a(2) xor b(2);
		p3 := a(3) xor b(3);
		
		g0 := a(0) and b(0);
		g1 := a(1) and b(1);
		g2 := a(2) and b(2);
		g3 := a(3) and b(3);
		
		c1 := g0 or (p0 and cin);
		c2 := g1 or (p1 and c1);
		c3 := g2 or (p2 and c2);
		cout <= g3 or (p3 and c3);
		
		output(0) <= p0 xor cin;
		output(1) <= p1 xor c1;
		output(2) <= p2 xor c2;
		output(3) <= p3 xor c3;

	end process;
end architecture;


library IEEE;
use IEEE.std_logic_1164.all;

entity Multiplier is
	port (
		a : in std_logic_vector(3 downto 0);
		b : in std_logic_vector(3 downto 0);
		y : out std_logic_vector(7 downto 0)
	);
end entity;

architecture behaviour of Multiplier is
	component Adder
		port (
			a      : in std_logic_vector(3 downto 0);
			b      : in std_logic_vector(3 downto 0);
			output : out std_logic_vector(3 downto 0);
			cin    : in std_ulogic;
			cout   : out std_ulogic
		);
	end component;
	
	signal s1, s2, s3, s4, o1, o2, o3, i1, i2 : std_logic_vector(3 downto 0);
	signal c1, c2, c3 : std_ulogic;
begin
	y(0) <= a(0) and b(0);
	
	s1 <= '0' & (a(3) and b(0)) & (a(2) and b(0)) & (a(1) and b(0));
	s2 <= (a(3) and b(1)) & (a(2) and b(1)) & (a(1) and b(1)) & (a(0) and b(1));
	s3 <= (a(3) and b(2)) & (a(2) and b(2)) & (a(1) and b(2)) & (a(0) and b(2));
	s4 <= (a(3) and b(3)) & (a(2) and b(3)) & (a(1) and b(3)) & (a(0) and b(3));
	
	Adder1 : Adder port map (a => s1, b => s2, output => o1, cin => '0', cout => c1);
	i1 <= c1 & o1(3) & o1(2) & o1(1);
	y(1) <= o1(0);
	Adder2 : Adder port map (a => s3, b => i1, output => o2, cin => '0', cout => c2);
	i2 <= c2 & o2(3) & o2(2) & o2(1);
	y(2) <= o2(0);
	Adder3 : Adder port map (a => s4, b => i2, output => o3, cin => '0', cout => c3);
	y(3) <= o3(0);
	y(4) <= o3(1);
	y(5) <= o3(2);
	y(6) <= o3(3);
	y(7) <= c3;
end architecture;