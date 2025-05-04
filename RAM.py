class RAM:  

    def __init__(self):  # create the constructor for the RAM class
        self.memoria = {}  # create a dictionary to store the data
        self.loading_mode = False  # used to avoid issues when an instruction exceeds the limit

    def set(self, addr: str, value: str):  # create a method to write to memory
        if len(addr) != 32 or len(value) != 32:  # check the length of the parameters and raise an error if they don't match
            raise IndexError("Address or value is not 32 bits")  
        direccion = int(addr, 2)  # convert the address to an integer
        if direccion % 4 != 0:  # check for 4-byte alignment; raise error if misaligned
            raise IndexError("Address not aligned (must be multiple of 4)")
        if direccion < 0 or direccion > 0xFFFFFFFF:  # ensure the address is within valid range; raise error if not
            raise IndexError("Address out of range")
        self.memoria[direccion] = value  # store the value at the specified address
        if direccion < 0x000F0000 and not self.loading_mode: 
            raise IndexError("Writing to instruction segment not allowed")  # ensure instructions do not exceed the permitted segment

    def get(self, addr: str):  # create a method to read from memory
        if len(addr) != 32:  # check the length of the address; raise error if invalid
            raise IndexError("Address is not 32 bits")
        direccion = int(addr, 2)  # convert the address to an integer
        if direccion % 4 != 0:  # check for 4-byte alignment; raise error if misaligned
            raise IndexError("Address not aligned (must be multiple of 4)")
        if direccion < 0 or direccion > 0xFFFFFFFF:  # ensure the address is within valid range; raise error if not
            raise IndexError("Address out of range")  
        if direccion in self.memoria:  # check if the address exists
            return self.memoria[direccion]  # return the stored value
        else:  # if not present
            return "0"*32  # return a default value of 32 zeros

    def reset(self):  # create a method to reset memory
        self.memoria.clear()  # clear all stored data

    def dump_instr(self, filename: str):  # create a method to dump instruction memory
        with open(filename, 'w') as f:  # open the file
            for addr in sorted(self.memoria):  # iterate over addresses in sorted order
                if addr < 0x000F0000:  # filter instruction addresses
                    f.write(f"0x{addr:08X} {self.memoria[addr]}\n")  # write in hexadecimal format

    def dump_data(self, filename: str):  # create a method to dump data memory
        with open(filename, 'w') as f:  # open the file
            for addr in sorted(self.memoria):  # iterate over addresses in sorted order
                if addr >= 0x000F0000:  # filter data addresses
                    f.write(f"0x{addr:08X} {self.memoria[addr]}\n")  # write in hexadecimal format

