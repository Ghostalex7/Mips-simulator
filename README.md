# MIPS Simulator – Python Implementation

[![Language: Python](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org/)  
A Python-based MIPS processor simulator capable of executing binary-encoded instructions with register and memory emulation.

---

## 📘 Description
This simulator is designed for educational purposes as part of a university-level computer architecture course. It emulates a simplified MIPS processor capable of executing machine code written directly in binary. Components include RAM, a register file, and a CPU core that mimics real MIPS control and execution flow.

---

## 🔧 Features
- Binary input execution without labels
- Support for key MIPS instructions: `add`, `lw`, `sw`, `beq`, `j`, `sll`, `srl`, `ori`, and more
- Separate memory segments for instructions and data
- PC (Program Counter) control and validation
- Register emulation: `$zero`, `$t0-$t7`, `$s0-$s7`, `PC`
- Exception handling for invalid memory access and misaligned addresses
- Dump functions to save memory and register states

---

## 🛠 Requirements
- Python 3.7 or higher

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Ghostalex7/mips-simulator.git
cd Mips-simulator
```

### 2. Prepare Input
Create or modify a file (e.g., `sample_program.txt`) with one binary instruction per line:
```
10001100000010010000000000000000
10001100000010100000000000000100
00000001001010100101100000100000
10101100000010100000000000000100
```

### 3. Run the Simulator
```bash
python3 sim.py 
```
After execution, the simulator will produce:
- `memory_dump.txt`: snapshot of memory data segment
- `registers_dump.txt`: state of all registers

---

## 📂 Project Structure
- `CPU.py` – Central class for instruction fetch/decode/execute
- `RAM.py` – Memory emulator with support for separate instruction/data segments
- `regs.py` – Register bank abstraction
- `utils.py` – Helper functions for binary/decimal conversions
- `sim.py` – Example usage script to run the simulator

---

## 💾 Instruction Set Supported
| Type    | Mnemonics         | Description                                |
|---------|-------------------|--------------------------------------------|
| R-type  | add, and, or, sll, srl | Arithmetic/logic operations              |
| I-type  | lw, sw, beq, bgtz, addi, andi, ori | Loads/stores, branching, immediates |
| J-type  | j                 | Jump to instruction address                |

All operations are executed from their raw binary encoding.

---

## 📦 Output Format
### `registers_dump.txt`
```
PC <value>
zero <value>
t0 <value>
t1 <value>
...
s7 <value>
```

### `memory_dump.txt`
```
0x000F0000 <value>
0x000F0004 <value>
...
```

---

## 🛡 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author
Ghostalex7 – [github.com/Ghostalex7](https://github.com/Ghostalex7)
