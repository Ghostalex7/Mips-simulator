from RAM import RAM  
from regs import Regs  
from utils import (  
    binario_a_decimal,
    binario_a_decimal_con_signo,
    decimal_a_binario,
    decimal_a_binario_con_signo
)

class CPU:

    def __init__(self): # create the constructor for the CPU class
        self.memory = RAM() # initialize the RAM class instance
        self.regs = Regs() # initialize the regs class instance

    def load_program(self, instructions): # create a method to load a program into memory
        self.memory.reset() # reset memory to its initial state
        self.regs.reset() # reset all registers
        addr = 0 # set the initial memory address
        self.memory.loading_mode = True # enable loading mode to avoid issues
        for instr in instructions: # iterate over each program instruction
            if addr > 0x0000FFFC:
                raise IndexError("Program exceeds maximum instruction size") # set a maximum instruction size limit
            bin_addr = decimal_a_binario(addr, 32) # convert address to 32-bit binary
            self.memory.set(bin_addr, instr) # store instruction in memory
            addr = addr + 4 # move to the next address (+4 bytes)
        self.memory.loading_mode = False # disable loading mode
        self.regs.set("PC", 0) # initialize the program counter to 0

    def map_reg(self, idx): # create method to map indices to register names
        if idx == 0: # case for zero register
            return "zero" # return the name of the zero register
        elif 8 <= idx <= 15: # case for temporary registers t0-t7
            return "t" + str(idx - 8) # calculate temporary register name
        elif 16 <= idx <= 23:  # case for saved registers s0-s7
            return "s" + str(idx - 16)  # calculate saved register name
        elif idx == 32: # special case for PC
            return "PC" # return name of PC register
        else: # if invalid index, raise an error
            raise IndexError("Invalid register")  

    def run_instrucion(self): # create method to execute one instruction
        pc_val = self.regs.get("PC") # get current PC value
        pc_bin = decimal_a_binario(pc_val, 32) # convert PC to 32-bit binary
        instr = self.memory.get(pc_bin) # get instruction from memory
        opcode = instr[0:6] # extract instruction opcode

        if opcode == "000000": # R-type instructions
            rs_bin = instr[6:11] # extract source register rs bits
            rt_bin = instr[11:16] # extract source register rt bits
            rd_bin = instr[16:21] # extract destination register rd bits
            funct  = instr[26:32] # extract function field for operation

            rs_idx = binario_a_decimal(rs_bin) # convert rs to numeric
            rt_idx = binario_a_decimal(rt_bin) # convert rt to numeric
            rd_idx = binario_a_decimal(rd_bin) # convert rd to numeric

            rs_name = self.map_reg(rs_idx) # get rs register name
            rt_name = self.map_reg(rt_idx) # get rt register name
            rd_name = self.map_reg(rd_idx) # get rd register name

            rs_val_bin = self.regs.get(rs_name) # get binary value of rs
            rt_val_bin = self.regs.get(rt_name) # get binary value of rt

            rs_val = binario_a_decimal_con_signo(rs_val_bin) # convert rs to signed value
            rt_val = binario_a_decimal_con_signo(rt_val_bin) # convert rt to signed value

            if funct == "100000": # ADD operation
                out = rs_val + rt_val # perform addition
                out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary
                self.regs.set(rd_name, out_bin) # store result in rd
            elif funct == "100010": # SUB operation
                out = rs_val - rt_val # perform subtraction
                out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary
                self.regs.set(rd_name, out_bin) # store result in rd
            elif funct == "100100": # AND operation
                out = rs_val & rt_val # perform logical AND
                out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary
                self.regs.set(rd_name, out_bin) # store result in rd
            elif funct == "100101": # OR operation
                out = rs_val | rt_val # perform logical OR
                out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary
                self.regs.set(rd_name, out_bin) # store result in rd
            elif funct == "000000": # SLL operation
                out = rt_val << rs_val # perform logical shift left
                out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary
                self.regs.set(rd_name, out_bin) # store result in rd
            elif funct == "000010": # SRL operation
                out = (rt_val % (1 << 32)) >> rs_val # perform logical shift right
                out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary
                self.regs.set(rd_name, out_bin) # store result in rd

        elif opcode == "100011": # LW instruction
            rs_idx = binario_a_decimal(instr[6:11]) # get base register index
            rt_idx = binario_a_decimal(instr[11:16]) # get destination register index
            imm_bin = instr[16:32] # extract immediate value

            imm = binario_a_decimal_con_signo(imm_bin) # convert immediate to signed
            base_bin = self.regs.get(self.map_reg(rs_idx)) # get base value
            base = binario_a_decimal_con_signo(base_bin) # convert base to signed

            addr = base + imm # calculate memory address
            addr_bin = decimal_a_binario(addr, 32) # convert address to binary

            val = self.memory.get(addr_bin) # get memory value
            self.regs.set(self.map_reg(rt_idx), val) # store value in register

        elif opcode == "101011":  # SW instruction
            rs_idx = binario_a_decimal(instr[6:11]) # get base register index
            rt_idx = binario_a_decimal(instr[11:16]) # get source register index
            imm = binario_a_decimal_con_signo(instr[16:32]) # convert immediate to signed

            base = binario_a_decimal_con_signo(self.regs.get(self.map_reg(rs_idx))) # get base value
            addr = base + imm # calculate memory address
            addr_bin = decimal_a_binario(addr, 32) # convert address to binary

            val = self.regs.get(self.map_reg(rt_idx)) # get register value
            self.memory.set(addr_bin, val) # store value in memory

        elif opcode == "001000":  # ADDI instruction
            rs_idx = binario_a_decimal(instr[6:11]) # get source register index
            rt_idx = binario_a_decimal(instr[11:16]) # get destination register index
            imm = binario_a_decimal_con_signo(instr[16:32]) # convert immediate to signed

            rs_val = binario_a_decimal_con_signo(self.regs.get(self.map_reg(rs_idx))) # get source value
            out = rs_val + imm # perform addition with immediate
            out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary

            self.regs.set(self.map_reg(rt_idx), out_bin) # store result in register

        elif opcode == "001100":  # ANDI instruction
            rs_idx = binario_a_decimal(instr[6:11]) # get source register index
            rt_idx = binario_a_decimal(instr[11:16]) # get destination register index
            imm = binario_a_decimal(instr[16:32]) # convert immediate (unsigned)

            rs_val = binario_a_decimal_con_signo(self.regs.get(self.map_reg(rs_idx))) # get source value
            out = rs_val & imm # perform logical AND
            out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary

            self.regs.set(self.map_reg(rt_idx), out_bin) # store result in register

        elif opcode == "001101": # ORI instruction
            rs_idx = binario_a_decimal(instr[6:11]) # get source register index
            rt_idx = binario_a_decimal(instr[11:16]) # get destination register index
            imm = binario_a_decimal(instr[16:32]) # convert immediate (unsigned)

            rs_val = binario_a_decimal_con_signo(self.regs.get(self.map_reg(rs_idx))) # get source value
            out = rs_val | imm # perform logical OR
            out_bin = decimal_a_binario_con_signo(out, 32) # convert result to binary

            self.regs.set(self.map_reg(rt_idx), out_bin) # store result in register

        elif opcode == "000100": # BEQ instruction
            rs_idx = binario_a_decimal(instr[6:11]) # get rs register index
            rt_idx = binario_a_decimal(instr[11:16]) # get rt register index
            imm = binario_a_decimal_con_signo(instr[16:32]) # convert offset

            rs_val = binario_a_decimal_con_signo(self.regs.get(self.map_reg(rs_idx))) # get rs value
            rt_val = binario_a_decimal_con_signo(self.regs.get(self.map_reg(rt_idx))) # get rt value

            if rs_val == rt_val: # compare register values
                new_pc = pc_val + 4 + (imm << 2) # calculate next PC
                self.regs.set("PC", new_pc) # update PC
                return # exit early

        elif opcode == "000111": # BGTZ instruction
            rs_idx = binario_a_decimal(instr[6:11]) # get rs register index
            imm = binario_a_decimal_con_signo(instr[16:32]) # convert offset

            rs_val = binario_a_decimal_con_signo(self.regs.get(self.map_reg(rs_idx))) # get rs value

            if rs_val > 0: # check if value is greater than zero
                new_pc = pc_val + 4 + (imm << 2) # calculate next PC
                self.regs.set("PC", new_pc) # update PC
                return # exit early

        elif opcode == "000010": # J instruction
            target = instr[6:32] + "00" # get jump target address
            new_pc = binario_a_decimal(target) # convert target to absolute address
            self.regs.set("PC", new_pc) # update PC with new address
            return  # exit early

        self.regs.set("PC", pc_val + 4) # update PC normally (+4 bytes)

    def run(self):  # create method to execute the full program
        while True: # run until an error occurs
            try: # try executing instructions
                self.run_instrucion() # execute one instruction
            except IndexError: # catch invalid access error
                break # stop execution if an error occurs

    def dump(self, reg_filename, mem_filename): # create method to save the state
        self.regs.dump(reg_filename) # save registers to file
        self.memory.dump_data(mem_filename) # save memory to file

