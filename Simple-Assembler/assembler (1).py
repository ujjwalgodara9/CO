from inspect import getframeinfo, stack
import time
from sys import stdin
from threading import Thread
called_lbl = []
hault_dic = {}
answer = None
lbl_hault = 0
jmp_hault = 0
is_haulted = 0
is_haulted2 = 0
is_haulted3 = 0
final_res = []
full_code = []
label_dic = {}
registers = {"r0": "000",
             "r1": "001",
             "r2": "010",
             "r3": "011",
             "r4": "100",
             "r5": "101",
             "r6": "110",
             "flags": "111"}
var_dic = {}
opcode = {
    "add": "00000",
    "sub": "00001",
    "movi": "00010",
    "mov": "00011",
    "ld": "00100",
    "st": "00101",
    "mul": "00110",
    "div": "00111",
    "rs": "01000",
    "ls": "01001",
    "xor": "01010",
    "or": "01011",
    "and": "01100",
    "not": "01101",
    "cmp": "01110",
    "jmp": "01111",
    "jlt": "10000",
    "jgt": "10001",
    "je": "10010",
    "hlt": "10011",

}
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


# def hault_label():
#     for x in label_dic:
#         if label_dic
#
#




def code(dict_name, i, line_no):
    i = i.lower()
    global errorflag
    not_to_be_in = [registers, var_dic, label_dic]
    found = 0
    if i == "flags":
        print("Error! illegal use of flags. line no: ", line_no)
        errorflag = 1
        return ""
    elif i in dict_name:
        temp = str(dict_name[i])
        found = 1
    elif dict_name in not_to_be_in:
        not_to_be_in.remove(dict_name)
    if found == 0:
        for each_dict in not_to_be_in:
            if i in each_dict:
                print("Error! wrong argumets. line no: ", line_no)
                errorflag = 1
                return ""
        if i in opcode:
            syn_error(line_no)
            errorflag = 1
        else:
            print("Error! undefined reg/var/label. line no: ", line_no)
            errorflag = 1
        return ""
    else:
        return temp



def toBinary(n, bits):
    val = str("{0:b}".format(int(n)))
    while len(val) < bits:
        val = "0" + val
    return val


def syn_error(line_no):
    global errorflag
    caller = getframeinfo(stack()[1][0])
    print("Error! (" + str(caller.lineno) + ") Wrong Syntax. line no: ", line_no)
    errorflag = 1


def print_type_a(ins, one, two, three, line_no):
    res = opcode[ins] + "00"
    for i in one, two, three:
        temp = code(registers, i, line_no)
        if temp == "":
            return
        else:
            res += temp
    final_res.append(res)


def print_type_b(ins, one, imm, line_no):
    res = opcode[ins]
    temp = code(registers, one, line_no)
    if temp == "":
        return
    else:
        res += temp
    res += imm
    final_res.append(res)


def print_type_c(ins, one, two, line_no):
    res = opcode[ins] + "00000"
    if ins == "mov" and two.lower() == "flags":
        temp = code(registers, one, line_no)
        if temp == "":
            return
        else:
            res += temp
        res += "111"
        final_res.append(res)
        return
    for i in one, two:
        temp = code(registers, i, line_no)
        if temp == "":
            return
        else:
            res += temp
    final_res.append(res)


def print_type_d(ins, one, var, line_no):
    res = opcode[ins]
    temp = code(registers, one, line_no)
    if temp == "":
        return
    else:
        res += temp
    temp = code(var_dic, var, line_no)
    if temp == "":
        return
    else:
        temp = "00000" + temp
        res += temp
    final_res.append(res)


def print_type_e(ins, lbl, line_no):
    res = opcode[ins] + "000"
    temp = code(label_dic, lbl, line_no)
    if temp == "":
        return
    else:
        res += temp
    final_res.append(res)


def print_type_f(ins):
    res = opcode[ins] + "00000000000"
    final_res.append(res)


def is_valid_name(name):
    one_alpha = 0
    for i in name:
        if i.isalnum():
            one_alpha = 1
    if one_alpha == 1:
        for i in name:
            if i.isalnum() or i == "_":
                pass
            else:
                return -1
    else:
        return -1
    return 1


def check_hault_lbl(instr_t,y):
    global  lbl_hault
    try:
        inst = instr_t[0]
    except:
        return ""
    if len(inst)<1:
        return ""
    str_0 = inst[0]
    # print("221",str_0)
    if str_0.endswith(":") and len(inst) == 2:
        temp = str_0[:-1]
        # print("224tmp",temp)
        if is_valid_name(temp) == -1:

            return ""

        found = 0
        if inst[1] == "hlt":
            # print("231 label detect")
            if y == 2:
                full_code.append(instr_t)
            for x in hault_dic:
                if hault_dic[x] == "hlt":

                    found = 1
                    # called_lbl.append(temp)
                    return x
            if found == 0:
                hault_dic.update({temp: inst[1]})
                lbl_hault = 1
    return ""


def check(instr_t, line_no, ins_no):
    global errorflag

    instr = instr_t[0]
    value = 0
    str_0 = instr[0]
    # print(instr)
    if str_0.endswith(":") and len(instr) > 1:
        # print("if")
        temp = str_0[:-1]
        if is_valid_name(temp) == -1:
            print("Error! invalid label name, line no: ",line_no)
            errorflag = 1
            return
        # if temp in label_dic:
        #     print("YEs")
        #     print(temp)
        #     print(label_dic[temp])
        #     print(toBinary(line_no, 8))
        #     print(label_dic)
        # print("264", instr[1])

        k = 0
        for x in final_res:
            if temp in x:
                final_res[k] = x.replace(temp, toBinary(ins_no, 8))
            k += 1
        if instr[1] == "hlt":
            print_type_f(instr[1])
            # print("266 hlt lbl appended")
            return
        # print("valid lbl")
        label_dic.update({temp: toBinary(ins_no, 8)})
        # print(label_dic)
        # print("updated")
        instr = instr[1:]
        try:
            str_0 = instr[0]
        except:
            syn_error(line_no)
            errorflag = 1
            return
    # else:
    #     syn_error(line_no)
    #     errorflag = 1
    #     return

    if str_0 == "var":
        if len(instr) == 2:
            var_dic.update({instr[1]: 0})
        else:
            syn_error(line_no)
            return -1

    if str_0 == "mov":
        if len(instr) == 3:
            if instr[2].startswith("$"):
                str_0 = "movi"
                try:
                    int(instr[2][1:])
                except:
                    syn_error(line_no)
                    return -1
                value = int(instr[2][1:])
                if value not in range(256):
                    print("Error! Illegal immediate value. line no: ", line_no)
                    errorflag = 1
        else:
            syn_error(line_no)
            return -1

    if str_0 in ("rs", "ls"):
        if len(instr) == 3:
            try:
                int(instr[2][1:])
            except:
                syn_error(line_no)
                return -1
            value = int(instr[2][1:])
            if value not in range(256):
                print("Error! Illegal immediate value. line no: ", line_no)
                errorflag = 1
                return -1
        else:
            syn_error(line_no)
            return -1

    if str_0 in type_a:
        if len(instr) == 4:
            print_type_a(str_0, instr[1], instr[2], instr[3], line_no)
        else:
            syn_error(line_no)
            return -1
    elif str_0 in type_b:
        if len(instr) == 3:
            print_type_b(str_0, instr[1], toBinary(value, 8), line_no)
        else:
            syn_error(line_no)
            return -1
    elif str_0 in type_c:
        if len(instr) == 3:
            print_type_c(str_0, instr[1], instr[2], line_no)
        else:
            syn_error(line_no)
            return -1
    elif str_0 in type_d:
        if len(instr) == 3:
            print_type_d(str_0, instr[1], instr[2], line_no)
        else:
            syn_error(line_no)
            return -1
    elif str_0 in type_e:
        if len(instr) == 2:
            lbl = instr[1]
            if is_valid_name(lbl):

                label_dic.update({lbl: lbl})
            else:
                print("Error! wrong label name, line no: ", line_no)
                errorflag = 1
                return -1
            print_type_e(str_0, instr[1], line_no)
        else:
            syn_error(line_no)
            return -1
    elif str_0.lower() == "hlt":
        if len(instr) == 1:
            # full_code.append(str_0)
            is_haulted = 1
            print_type_f(str_0)
            return 1
        else:
            print("Error! wrong hlt syntax. line no: ", line_no)
            errorflag = 1
            return -1
    else:
        print("Error! typo. line no: ", line_no)
        errorflag = 1

errorflag = 0


def main():
    global is_haulted2
    global is_haulted3
    global lbl_hault
    global jmp_hault
    global called_lbl
    global errorflag
    global final_res
    total_lines = 0
    num = 0
    global full_code
    # full_code = []
    global is_haulted
    instr_declared = 0
    var_lines = 0
    for i in range(256):
        instr = [[]]
        if lbl_hault == 1 and jmp_hault == 1:
            # print("398YYY")
            break



        try:
            instr = [input().split()]
        except:
            pass
        # print("407",instr)
        if len(instr[0])>1:
            check_hault_lbl(instr,2)
        # print("check called")
        # if check
        try:
            if instr[0][0] in type_e:
                # print("WWw")
                # print("411append",instr[0][1])
                called_lbl.append(instr[0][1])
        except:
            pass
            # print(instr[0][1])
        # print("415",instr[0][0])
        b = check_hault_lbl(instr,1)
        # print("bb",b)
        if b in called_lbl:
            # print("b",b)
            is_haulted2 = 1
            jmp_hault = 1
            # print("broke")
            break

        # print("dsfsdf")
        if len(instr[0])==0 or is_haulted:
             break
        if instr[0][0]=="hlt":
            if is_haulted3 == 1:
                full_code.append(instr)
                errorflag = 1
                break
            full_code.append(instr)
            is_haulted3 = 1
            # print("breaking")
            continue
        if instr[0][0] != "var":
            full_code.append(instr)
            total_lines += 1
            num += 1
            instr_declared = 1

        else:
            if instr_declared == 1 or is_haulted == 1 or is_haulted3 == 1:
                print("error! cant use var after instructions or hlt, line no: ", num)
                errorflag = 1
                return
            if instr[0][1] not in var_dic:
                if instr[0][1] not in registers:
                    val = instr[0][1]
                    if is_valid_name(val) == -1:
                        print("Error! invalid var name, line no: ", num)
                        errorflag = 1
                        return
                    var_dic.update({val: 0})
                    num += 1
                    var_lines += 1
                else:
                    print("Error! can't use register/flags in var. line no: ", num)
                    errorflag = 1
                    return
            else:
                print("Error! Redeclaring variable. line no: ", num)
                errorflag = 1
                return
    temp = total_lines + 1
    for values in var_dic:
        var_dic[values] = toBinary(temp, 3)
        temp += 1
    # print("num=",num)
    ins_no = 0
    i = var_lines
    hault_flag = 0

    for line in full_code:
        # print("479",line)
        if is_haulted == 1:
            print("Error! instructions wirtten after hault. line no: ", i)
            errorflag = 1
            return
        else:
            # print(line)
            hault_flag = check(line, i, ins_no)
            if hault_flag == 1:
                is_haulted = 1
            i += 1
            ins_no += 1
    for line in final_res:
        flag = 0
        # line = line[0]
        for r in line:
            if not r.isnumeric():
                print("Error! label not defined, line no: ", i)
                flag = 1
                errorflag = 1
                break
        if flag == 1:
            break

    if is_haulted == 0 and is_haulted2 == 0:
        print("Error! missing hlt. line no: ", i)
        errorflag = 1
        return
    elif errorflag == 0:
        for i in final_res:
            print(i)


if __name__ == '__main__':
    main()
