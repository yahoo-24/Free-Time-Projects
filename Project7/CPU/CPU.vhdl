library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Mux3Way8Bit is
    port (
        sel : in std_logic_vector(1 downto 0); -- 2-bit select signal
        a   : in std_logic_vector(7 downto 0); -- 8-bit input a
        b   : in std_logic_vector(7 downto 0); -- 8-bit input b
        c   : in std_logic_vector(7 downto 0); -- 8-bit input c
        y   : out std_logic_vector(7 downto 0) -- 8-bit output y
    );
end Mux3Way8Bit;

architecture Behavioral of Mux3Way8Bit is
begin
    process(sel, a, b, c)
    begin
        case sel is
            when "00" =>
                y <= a;
            when "01" =>
                y <= b;
            when "10" =>
                y <= c;
            when others =>
                y <= (others => '0'); -- default case to handle unused state
        end case;
    end process;
end Behavioral;



library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity CPU is
	port (
		status    : out std_ulogic;
		CheckRAM  : out std_logic_vector(7 downto 0);
		CheckALU  : out std_logic_vector(7 downto 0);
		clk       : in std_ulogic;
		out1      : out std_logic_vector(7 downto 0);
		out2      : out std_logic_vector(7 downto 0);
		in1       : out std_logic_vector(7 downto 0)
	);
end CPU;

architecture behave of CPU is
	component ALU16
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
	end component;
	
	component RAM128
		port (
			input   : in std_logic_vector(7 downto 0);
			output  : out std_logic_vector(7 downto 0);
			address : in std_logic_vector(2 downto 0);
			load    : in std_ulogic;
			clk     : in std_ulogic
		);
	end component;
	
	component RAM8
		port (
			input    : in std_logic_vector(7 downto 0);
			output1  : out std_logic_vector(7 downto 0);
			output2  : out std_logic_vector(7 downto 0);
			address  : in std_logic_vector(2 downto 0);
			load     : in std_ulogic;
			address1 : in std_logic_vector(2 downto 0);
			address2 : in std_logic_vector(2 downto 0);
			clk      : in std_ulogic
		);
	end component;
	
	component Mux3Way8Bit
		port (
			sel : in std_logic_vector(1 downto 0); -- 2-bit select signal
			a   : in std_logic_vector(7 downto 0); -- 8-bit input a
			b   : in std_logic_vector(7 downto 0); -- 8-bit input b
			c   : in std_logic_vector(7 downto 0); -- 8-bit input c
			y   : out std_logic_vector(7 downto 0) -- 8-bit output y
		);
	end component;
	
	type instruction is array (0 to 7) of std_logic_vector(15 downto 0);
	signal ins : instruction  := ("0110000110110101", "0110000100100110", "0010110111101110", "1000000010100111",
	"0000000000000000", "0000000000000000", "0000000000000000", "0000000000000000");
	
	signal i : integer := 0;
	signal ld, st : std_ulogic;
	signal op : std_logic_vector(15 downto 0);
	signal reg, resultALU, muxed, resultRAM, o1, o2 : std_logic_vector(7 downto 0);
	signal addr, addr1, addr2 : std_logic_vector(2 downto 0) := "000";
	signal mem : std_logic_vector(2 downto 0) := "000";
	signal code : std_logic_vector(3 downto 0) := "1111";
	signal x : std_logic_vector(1 downto 0) := "11";
	
	signal statusN, statusV, statusC, statusZ : std_ulogic; 
	
begin
	process (clk)
	begin
		if rising_edge(clk) then
			op <= ins(i);
			i <= i + 1;
			if (op(15) = '0' and op(14) = '1' and op(13) = '1') then
				-- Load value directly
				ld <= '1';
				st <= '0';
				reg <= op(10 downto 3);
				addr <= op(2 downto 0);
				x <= "00";
			elsif (op(15) = '0' and op(14) = '1' and op(13) = '0') then
				-- Load from memory
				ld <= '1';
				st <= '0';
				mem <= op(5 downto 3);
				addr <= op(2 downto 0);
				x <= "01";
			elsif (op(15) = '1' and op(14) = '0' and op(13) = '0') then
				-- Store
				ld <= '0';
				st <= '1';
				mem <= op(5 downto 3);
				addr1 <= op(2 downto 0);
			elsif (op(15) = '0' and op(14) = '0' and op(13) = '1') then
				-- Operation
				ld <= '1';
				st <= '0';
				code <= op(12 downto 9);
				addr1 <= op(5 downto 3);
				addr2 <= op(2 downto 0);
				addr <= op(8 downto 6);
				x <= "10";
			else
				ld <= '0';
				st <= '0';
			end if;
		end if;
	end process;
	
	RegisterBank : RAM8 port map(
		input => muxed,
		output1 => o1,
		output2 => o2,
		address => addr,
		load => ld,
		address1 => addr1,
		address2 => addr2,
		clk => clk
	);
	
	ALU : ALU16 port map (
		a => o1,
		b => o2,
		opcode => code,
		V => statusV,
		N => statusN,
		Z => statusZ,
		C => statusC,
		result => resultALU
	);
	
	RAM : RAM128 port map (
		input => o1,
		output => resultRAM,
		address => mem,
		load => st,
		clk => clk
	);
	
	Mux : Mux3Way8Bit port map (
		sel => x,
		a => reg,
		b => resultRAM,
		c => resultALU,
		y => muxed
	);
	
	status <= statusN or statusV or statusZ or statusC;
	CheckRAM <= resultRAM;
	CheckALU <= resultALU;
	out1 <= o1;
	out2 <= o2;
	in1 <= muxed;
	
end behave;