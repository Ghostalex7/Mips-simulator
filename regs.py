from utils import binario_a_decimal 

class Regs:  

    def __init__(self):  # initialize the constructor of the Regs class
        self.registers = {"zero": "0"*32, "PC": 0}  # initialize the 'zero' register with 32 bits and the PC
        for i in range(8):  # create temporary registers t0–t7
            self.registers[f"t{i}"] = "0"*32  # initialize each t register with 32 zeros
        for i in range(8):  # create saved registers s0–s7
            self.registers[f"s{i}"] = "0"*32  # initialize each s register with 32 zeros

    def set(self, reg_idx: str, value):  # method to set the value of a register
        if reg_idx not in self.registers:  # if register does not exist, raise an error
            raise IndexError("Invalid register")  
        if reg_idx == "zero":  # special case for 'zero' register
            return  # do nothing to preserve immutability of zero
        if reg_idx == "PC":  # special case for the Program Counter
            if isinstance(value, int):  # if given an integer, store it directly
                self.registers["PC"] = value
            elif isinstance(value, str):  # if given a binary string
                if len(value) != 32:  # ensure it's 32 bits; raise error if not
                    raise ValueError("PC only accepts 32-bit binary")
                for c in value:  # check each character
                    if c not in ("0", "1"):  # only allow valid binary characters
                        raise ValueError("PC only accepts 32-bit binary")
                self.registers["PC"] = binario_a_decimal(value)  # convert to decimal and store
            else:  # if value is of invalid type, raise an error
                raise ValueError("PC only accepts int or 32-bit binary") 
            return  # finish execution for PC
        if not isinstance(value, str):  # all other registers require a string; raise error if not
            raise ValueError("Register must be a 32-bit binary string")
        if len(value) != 32:  # check if binary string is 32 bits long
            raise ValueError("Register must be a 32-bit binary string")
        for c in value:  # verify each character in the string
            if c not in ("0", "1"):  # raise error if any character is invalid
                raise ValueError("Register must be a 32-bit binary string") 
        self.registers[reg_idx] = value  # store the valid value in the register

    def get(self, reg_idx: str):  # method to get the value of a register
        if reg_idx not in self.registers:  # raise error if register does not exist
            raise IndexError("Invalid register") 
        return self.registers[reg_idx]  # return the value of the register

    def reset(self):  # method to reset all registers
        for key in self.registers:  # iterate over all register keys
            if key == "PC":  # special case for PC
                self.registers[key] = 0  # reset PC to integer 0
            elif key != "zero":  # skip the 'zero' register
                self.registers[key] = "0"*32  # reset all others to 32 zeros

    def dump(self, filename):  # method to save register state to a text file
        with open(filename, 'w') as f:  # open the file
            orden = ["PC", "zero"] + [f"t{i}" for i in range(8)] + [f"s{i}" for i in range(8)]
            for reg in orden:  # write each register in the specified order
                f.write(f"{reg} {self.registers[reg]}\n")  # write register name and value

