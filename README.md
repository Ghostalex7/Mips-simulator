# MIPS Simulator

[![Language: Python](https://img.shields.io/badge/language-python-blue.svg)](https://www.python.org/)  
A Python-based MIPS processor simulator capable of executing binary-encoded instructions with support for register management, memory segmentation, and instruction decoding.

---

## 📘 Description

This project is a simulation of a MIPS processor, developed as part of a coursework assignment for a computer architecture class. It emulates the behavior of a MIPS processor that executes programs written in binary machine code. The simulator interprets instructions, decodes them according to MIPS formats (R, I, J), updates registers and memory accordingly, and handles jumps and branches.

---

## 🧩 Features

- Instruction decoding based on opcode and funct fields
- Memory and register file simulation
- Support for MIPS instruction types: arithmetic, logic, shift, branch, jump, load/store
- Validity checks for memory addressing (32-bit aligned, valid ranges)
- Exception handling for invalid accesses
- Instruction stepping and full execution flow

---

## ⚙️ Requirements

- Python 3.7 or higher

---

## 🛠 Setup & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ghostalex7/mips-simulator.git
   cd mips-simulator
   ```

2. **Prepare your binary input program:**
   - Include your binary instructions (one per line) in a file such as `sample_program.txt`

3. **Run the simulator:**
   ```bash
   python3 sim.py sample_program.txt
   ```

> Make sure all core files (`CPU.py`, `RAM.py`, `regs.py`, `utils.py`) are in the same directory.

---

## 📁 Project Files

- `CPU.py` – Main processor logic
- `RAM.py` – Memory interface with instruction/data segments
- `regs.py` – Register file class with symbolic names
- `utils.py` – Helper functions for instruction processing (optional)
- `sim.py` – Runner script that loads a binary program and simulates execution
- `sample_program.txt` – Example binary MIPS program

---

## 📄 Supported Instructions

| Category | Instruction | Type | Opcode | Funct (if R-type) |
|----------|-------------|------|--------|------------------|
| Load     | `lw`        | I    | 0x23   | -                |
| Store    | `sw`        | I    | 0x2B   | -                |
| Arithmetic | `add`, `addi` | R/I | 0x00 / 0x08 | 0x20         |
| Logical  | `and`, `andi`, `or`, `ori` | R/I | 0x00 / 0x0C / 0x0D | 0x24 / 0x25 |
| Shift    | `sll`, `srl` | R    | 0x00   | 0x00 / 0x02      |
| Branch   | `beq`, `bgtz` | I   | 0x04 / 0x07 | -            |
| Jump     | `j`         | J    | 0x02   | -                |

---

## 🚨 Memory Architecture

- Instruction Segment: `0x00000000` – `0x0000FFFC`
- Data Segment: Starts at `0x000F0000`
- All accesses must be word-aligned (multiples of 4)
- Access outside defined ranges raises `IndexError`

---

## 🧪 Example Input

```
10001100000010010000000000000000
10001100000010100000000000000100
00000001001010100101100000100000
10101100000010100000000000000100
```

Which corresponds to:
```
0x00000000: lw $t1, 0($zero)
0x00000004: lw $t2, 4($zero)
0x00000008: add $t3, $t1, $t2
0x0000000C: sw $t2, 4($zero)
```
---

## 🛡 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Ghostalex7 – [github.com/Ghostalex7](https://github.com/Ghostalex7)
