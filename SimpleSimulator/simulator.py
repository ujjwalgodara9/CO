code = []
type_a = ("add",
          "sub",
          "mul",
          "xor",
          "or",
          "and")
type_b = ("movi",
          "rs",
          "ls")
type_c = ("mov",
          "div",
          "not",
          "cmp")
type_d = ("ld",
          "st")
type_e = ("jmp",
          "jlt",
          "jgt",
          "je")
registers = {"r0": "0b0000000000000000",
             "r1": "0b0000000000000000",
             "r2": "0b0000000000000000",
             "r3": "0b0000000000000000",
             "r4": "0b0000000000000000",
             "r5": "0b0000000000000000",
             "r6": "0b0000000000000000",
             "flags": "0000"}
opcode_dic = {'00000': 'add',
              '00001': 'sub',
              '00010': 'movi',
              '00011': 'mov',
              '00100': 'ld',
              '00101': 'st',
              '00110': 'mul',
              '00111': 'div',
              '01000': 'rs',
              '01001': 'ls',
              '01010': 'xor',
              '01011': 'Or',
              '01100': 'And',
              '01101': 'not',
              '01110': 'cmp',
              '01111': 'jmp',
              '10000': 'jlt',
              '10001': 'jgt',
              '10010': 'je',
              '10011': 'hlt'}
opcode_smbl = {"add": "+",
               "sub": "-",
               "mul": "*",
               "xor": "^",
               "or": "|",
               "and": "&",
               "movi": "=",
               "rs": ">>",
               "ls": "<<"}
registers_add = {"000": "r0",
                 "001": "r1",
                 "010": "r2",
                 "011": "r3",
                 "100": "r4",
                 "101": "r5",
                 "110": "r6",
                 "111": "flags"}
# flags = "0000000000000000"


def toBinary(n, bits):
    val = str("{0:b}".format(int(n)))
    while len(val) < bits:
        val = "0" + val
    return val


def rf_dump():
    for x in registers:
        if x == "flags":
            print(registers[x].zfill(16),end=" ")
        else:
            print(registers[x][2:].zfill(16),end=" ")
    print()


def mem_dump():
    for x in code:
        print(x)


def do_type_a(line, smbl):
    # first get name of mentioned registers
    t_r1, t_r2, t_r3 = registers_add[line[7:10]], registers_add[line[10:13]], registers_add[line[13:16]]
    res = eval("int(registers[t_r2],2)" + smbl + "int(registers[t_r3],2)")  # calc all a type instr
    if res > 65535 or res < 0:  # checking overflow
        registers.update({"flags": "1000"})  # set overflow flag
        registers.update({t_r1: bin(0)})
    else:
        registers.update({"flags": "0000"})  # else reset flag
        registers.update({t_r1: bin(res)})  # and update registers


def do_type_b(line, smbl):
    res = 0
    t_r1, imm = registers_add[line[5:8]], int(line[8:16], 2)
    t_r1_val = int(registers[t_r1], 2)
    if smbl == "=":
        res = imm
    else:
        res = eval("t_r1_val " + smbl + " imm")
    registers.update({t_r1: bin(res)})


def do_type_c(line):
    instruction = opcode_dic[line[:5]]
    t_r1, t_r2 = registers_add[line[10:13]], registers_add[line[13:16]]
    if instruction == "mov":
        registers.update({t_r1: bin(int(registers[t_r2], 2))})
    elif instruction == "div":
        quotient = bin(int(registers[t_r1], 2) // int(registers[t_r2], 2))
        remainder = bin(int(registers[t_r1], 2) % int(registers[t_r2], 2))
        registers.update({"r0": quotient})
        registers.update({"r1": remainder})
    elif instruction == "not":
        val = registers[t_r2][2:]
        new_val = "0b"
        for x in val:
            if x == "0":
                new_val += "1"
            else:
                new_val += "0"
        registers.update({t_r1: new_val})
    elif instruction == "cmp":
        if int(registers[t_r1], 2) > int(registers[t_r2], 2):
            registers.update({"flags": "0010"})
        elif int(registers[t_r1], 2) < int(registers[t_r2], 2):
            registers.update({"flags": "0100"})
        elif int(registers[t_r1], 2) == int(registers[t_r2], 2):
            registers.update({"flags": "0001"})
    # print(registers)


def do_type_d(line):
    t_r1, mem_add = registers_add[line[5:8]], int(line[8:16], 2)
    instruction = opcode_dic[line[:5]]
    if instruction == "ld":
        registers.update({t_r1: bin(mem_add)})
    else:
        code[mem_add] = registers[t_r1][2:].zfill(16)


def do_type_e(line):
    jmp_mem_add = int(line[8:16], 2)
    instruction = opcode_dic[line[:5]]
    if instruction == "jmp":
        execute(code[jmp_mem_add])
    elif instruction == "jlt" and registers["flags"] == "0100":
        execute(code[jmp_mem_add])
    elif instruction == "jgt" and registers["flags"] == "0010":
        execute(code[jmp_mem_add])
    elif instruction == "je" and registers["flags"] == "0001":
        execute(code[jmp_mem_add])


def execute(line):
    # instruction = add, or, mul ....
    instruction = opcode_dic[line[:5]]
    # print(instruction)
    if instruction in type_a:
        do_type_a(line, opcode_smbl[instruction])
    elif instruction in type_b:
        do_type_b(line, opcode_smbl[instruction])
    elif instruction in type_c:
        do_type_c(line)
    elif instruction in type_d:
        do_type_d(line)
    elif instruction in type_e:
        do_type_e(line)
    if instruction not in ("cmp", "add"):
        registers.update({"flags": "0000"})  # reset flag
    if instruction == "hlt":
        return True
    else: return False


def main():
    global code
    for x in range(256):
        code.append("0000000000000000")
    counter = 0
    # following 6 lines read lines from input till EOF and stores in 'code' as list of str
    for x in range(256):
        try:
            line = input()
            if line == '':
                break
            code[counter] = line
        except:
            pass
        counter += 1
    pc = 0
    halted = False
    while not halted:
        line = code[pc]
        halted = execute(line)
        # print(halted)
        # halted = True
        print(toBinary(pc,8), end=" ")
        rf_dump()
        pc += 1
    mem_dump()

if __name__ == '__main__':
    main()
