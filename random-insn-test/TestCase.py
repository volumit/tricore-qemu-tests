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
import os
from random import randint
from Config import *
from InstructionList import insn
from Instruction import JumpOffset, jumpMarkerList
from Utils import print_out

class TestCase:

    num_insn = None

    def __init__(self, name, num_insn):
        global jumpMarkerList

        list_len = len(insn) -1
        self.name = name
        self.num_insn = num_insn
        if not os.path.isdir(name):
            os.mkdir(name)
        else:
            os.system("rm -f "+name+"/"+name+".*")

        with open(name+"/"+name+".s", "a") as f:
            # generate intro
            f.write(".text\n")
            f.write(".global _start\n")
            f.write("_start:\n")
            f.write("mov %d" + str(baseJumpReg) + ", 7\n")
            f.write("add %d"+ str(baseJumpReg) + ", 3\n")
            f.write("sh %d"+ str(baseJumpReg) + ", 7\n")
            f.write("sh %d"+ str(baseJumpReg) + ", 7\n")
            f.write("sh %d"+ str(baseJumpReg) + ", 7\n")
            f.write("sh %d"+ str(baseJumpReg) + ", 7\n")
            f.write("mov.a %a"+ str(baseJumpReg) + ",%d"+ str(baseJumpReg) +" \n")
            f.write("mov %d"+ str(baseJumpReg) + ", 0 \n")
            # setup mem register
            f.write("mov %d" + str(baseMemReg) + " 13\n")
            f.write("sh %d"+ str(baseMemReg) + ", 7\n")
            f.write("sh %d"+ str(baseMemReg) + ", 7\n")
            f.write("sh %d"+ str(baseMemReg) + ", 7\n")
            f.write("add %d" +str(baseMemReg) +", 7\n")
            f.write("sh %d"+ str(baseMemReg) + ", 7\n")
            f.write("mov.a %a"+ str(baseMemReg) + ",%d"+ str(baseMemReg) +" \n")
            f.write("mov %d"+ str(baseMemReg) + ", 0 \n")
            f.write("# test starts here --------------\n")
            # generate test
            for i in range(0, num_insn):
                f.write(self.generate(i))
            f.write("# test ends here --------------\n")
            # generate outro
            f.write("movh %d15,hi:0x0000900d\n")
            f.write("addi %d15,%d15,lo:0x0000900d\n")
            f.write("mov.a %a14,%d15\n");
            f.write("label"+str(num_insn) +":debug\n")
            f.write("j label"+str(num_insn)+"\n")


    def generate(self, num):
        global jumpMarkerList
        result = ""
        # if we generated a label pointing to this pc..
        if num in jumpMarkerList:
            # .. we need to generate it here
            result = jumpMarkerList[num].getString()

        r = randint(0, len(insn)-1)
        # if we have a jump insn we need to init the JumpOffset first,
        # since it needs to know the current pc for the max_range
        # calculation
        for field in insn[r].insn_fields:
            if isinstance(field, JumpOffset):
                field.init(num, self.num_insn)

        result = result + insn[r].get_asm()+"\n"

        return result

    def compile(self):
        global tas, tld, tld_flags
        global tas_flags
        global version
        #print_out("Compiling "+ self.name)
        # asm
        print_out("Assemble " + tas + " " + tas_flags + " " + self.name+"/"+self.name+".s -o" + self.name+"/"+self.name+".o")
        os.system(tas + " " + tas_flags + " " + self.name+"/"+self.name+".s -o" + self.name+"/"+self.name+".o")
        # ld
        ld_str = "{ld} {ld_flags} {name}/{name}.o -o {name}/{name}.elf".format(ld=tld, ld_flags=tld_flags, name=self.name)
        print_out("Link " + ld_str)
        os.system(ld_str)
        print_out("Dissassemble " + tobjdump + " " + tobjdump_flags + " " + self.name+"/"+self.name+".elf"+ " >"+self.name+"/"+self.name+".lst")
        os.system(tobjdump + " " + tobjdump_flags + " " + self.name+"/"+self.name+".elf"+ " >"+self.name+"/"+self.name+".lst")


    def runTSIM(self):
        global tsim
        global tsim_flags
        global version
        #print_out("Running TSIM for " + self.name)

        exe = "cd " + self.name + "&&" +                 \
              tsim + " " + tsim_flags + " " + self.name +".elf"

        print_out("Running TSIM "+exe)
        os.system(exe)
        os.system("mv " + self.name + "/Sim.traceinstr " + self.name  + "/tsim.result")

    def runQEMU(self):
        global qemu
        global qemu_flags
        print_out("Running QEMU for " + self.name)

        f = open(self.name+"/run_qemu.sh", "w")

        movdir = "cd {}".format(self.name)
        qemu_cmd = "{QEMU} {QEMU_FLAGS} -kernel {test}.elf ".format(test=self.name, QEMU=qemu, QEMU_FLAGS=qemu_flags)
        exe = "{} && {}".format(movdir, qemu_cmd)
        f.write("#!/bin/sh\n")
        f.write(qemu_cmd)
        f.close()
        os.system("chmod u+x "+self.name+"/run_qemu.sh")
        os.system(exe + " > /dev/null")

    def compareResults(self):
        print_out("Comparing results for " + self.name)
        os.system("python2 EvaluateResults.py " + self.name + "/tsim.result " + self.name + "/qemu.result >" + self.name + "/result.txt")

    def evaluateSucess(self):
        f = open(self.name+"/result.txt")
        line = f.readline()
        f.close()
        if "Test successful" in line:
            return 1
        return 0

