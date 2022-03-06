#!/usr/bin/env python2
"""
  Copyright (c) 2017 Bastian Koppelmann Paderborn University

 This library is free software; you can redistribute it and/or
 modify it under the terms of the GNU Lesser General Public
 License as published by the Free Software Foundation; either
 version 2 of the License, or (at your option) any later version.

 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public
 License along with this library; if not, see <http://www.gnu.org/licenses/>.
"""

import os,sys,re

error = 0

def printhelp():
    print "USAGE: evaluate_results.py [options] TSIMDUMP QEMUDUMP"

def findQemuLineByNum(number):
    idx = int(number)+1
    return qemudata.split("Trace")[idx].strip()

def findTsimInsn(line):
        result = list()
        string = "\t"
        insn_pos = line.find(string)
        if insn_pos == 0:
               return "Insn Not Found"
        insn_pos = insn_pos+10
        insn_end = line.find(string,insn_pos)
        if insn_end == 0:
               return "Insn Not Found"
        return line[insn_pos:insn_end]

#take only wb registers into account
def findTsimRegA(line):
        result = list()
        string = "wb:"
        reg_pos_wb = line.find(string)
        if reg_pos_wb == 0:
               return result
        
        for i in range(0,16):
                string = "a"+str(i)+"["
                reg_pos = line.find(string,reg_pos_wb)
                if reg_pos > 0:
                        reg_pos = reg_pos +2+len(str(i))
                result.append(reg_pos)

        return result

def findTsimRegD(line):
        result = list()
        string = "wb:"
        reg_pos_wb = line.find(string)
        if reg_pos_wb == 0:
               return result
        
        for i in range(0,16):
                string = "d"+str(i)+"["
                reg_pos = line.find(string,reg_pos_wb)
                if reg_pos > 0:
                        reg_pos = reg_pos +2+len(str(i))
                result.append(reg_pos)

        return result


def getQemuRegAValue(line,reg):
    string = "a"+str(reg)+"["
    startpos = line.find(string)+2+len(str(reg))
    endpos = line.find("]",startpos)
    if "[" in line[startpos:endpos]:
        print "ERROR"

    return line[startpos:endpos]

def getQemuRegDValue(line,reg):
        string = "d"+str(reg)+"["
        startpos = line.find(string)+2+len(str(reg))
        endpos = line.find("]",startpos)
        return line[startpos:endpos]

class QEMULogEntry:
    def __init__(self, a, d, psw, pc):
       self.a = a
       self.d = d
       self.psw = psw
       self.pc = pc

    def __str__(self):
        return "PC: 0x{}\nPSW=0x{}\nGPR_A={}\nGPR_D={}".format(hex(self.pc),
            hex(self.psw), ["0x{}".format(hex(ai)) for ai in self.a],
            ["0x{}".format(hex(di)) for di in self.d])


prev_pc = 0xa0000000
def parseQEMULine(line):
    global prev_pc
    a_regs = list()
    d_regs = list()

    for l in xrange(0, 16, 4):
        regex = r'GPR A' + str(l).zfill(2) +': ([0-9a-fA-F]+) ([0-9a-fA-F]+) ([0-9a-fA-F]+) ([0-9a-fA-F]+)'
        m = re.search(regex, line)
        for i in range(1,5):
            a_regs.append(int(m.group(i), 16))

    for l in xrange(0, 16, 4):
        regex = r'GPR D' + str(l).zfill(2) +': ([0-9a-fA-F]+) ([0-9a-fA-F]+) ([0-9a-fA-F]+) ([0-9a-fA-F]+)'
        m = re.search(regex, line)
        for i in range(1,5):
            d_regs.append(int(m.group(i), 16))

    regex = r'PSW: ([0-9a-fA-F]+)'
    m = re.search(regex, line)
    psw = int(m.group(1), 16)

    ret = QEMULogEntry(a_regs, d_regs, psw, prev_pc)

    regex = r'PC: ([0-9a-fA-F]+)'
    m = re.search(regex, line)
    prev_pc = int(m.group(1), 16)
    return ret

def compareRegA(tsimline,qemuline,linenum):
    global error
    i = 0
    for startpos in findTsimRegA(tsimline):
        if startpos <> -1:
            endpos = tsimline.find("]",startpos)
            qemuvalue = qemuline.a[i]
            if int(tsimline[startpos:endpos].strip(),16) <> qemuvalue:
                error = error +1
                print "Error at Instruction "+str(linenum) + " PC: " + str(hex(qemuline.pc)) + " a["+str(i)+"] tsim =" + tsimline[startpos:endpos].strip() + ", qemu =" + str(hex(qemuvalue)) + " " + findTsimInsn(tsimline)
        i = i+1


def compareRegD(tsimline,qemuline,linenum):
    global error
    i = 0
    for startpos in findTsimRegD(tsimline):
        if startpos <> -1:
            endpos = tsimline.find("]",startpos)
            qemuvalue = qemuline.d[i]
            if int(tsimline[startpos:endpos].strip(),16) <> qemuvalue:
                error = error +1
                print "Error at Instruction "+str(linenum) + " PC: " + str(hex(qemuline.pc)) + " d["+str(i)+"] tsim =" + tsimline[startpos:endpos].strip() + ", qemu =" + str(hex(qemuvalue))+ " " + findTsimInsn(tsimline)
        i = i+1

def comparePSW(tsimline, qemuline, linenum):
    global error

    tsim_start_pos = tsimline.find("psw:") + 4
    psw_tsim = tsimline[tsim_start_pos:].strip()

    psw_qemu = qemuline.psw

    if int(psw_tsim,16) <> psw_qemu:
        error = error +1
        print "Error at Instruction "+str(linenum) + " PC: " + str(hex(qemuline.pc)) + " PSW: tsim =" + str(psw_tsim) + ", qemu =" + str(hex(psw_qemu)) + " " + findTsimInsn(tsimline)

if len(sys.argv) < 3:
    printhelp()
    sys.exit(0)

tsimf = open(sys.argv[1],"r")
qemuf = open(sys.argv[2],"r")

tsimdata = tsimf.readlines()
qemudata = qemuf.read()

tsimline = str(tsimdata[0])
for tsimline in tsimdata[:-1]:
    addresspos_start = int(tsimline.find("\t"))
    addresspos_end = int(tsimline.find("\t",addresspos_start+1))

    tsimaddress = tsimline[addresspos_start+1:addresspos_end]
#    tsiminst_num = tsimline[0:tsimline.find("(")]
#newer tsim versions have "VMO " as lead in the line
    tsiminst_num = tsimline[4:tsimline.find("(")]
    qemuline = findQemuLineByNum(tsiminst_num)
    ctx = parseQEMULine(qemuline)
    compareRegA(tsimline,ctx,tsiminst_num)
    compareRegD(tsimline,ctx,tsiminst_num)
    comparePSW(tsimline,ctx, tsiminst_num)
if error == 0:
    print "Test successfull"
