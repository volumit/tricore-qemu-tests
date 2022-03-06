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
from Config import *
from random import randint
from Utils import print_out

jumpMarkerList = dict()

class InstructionField:

    name = ""

    def __init__(self, n):
        self.name = n

    def getString(self):
        return self.name

class Register(InstructionField):

    def __init__(self, name):
        global lastRegister
        self.name = "%"+name
        lastRegister = self

def getnextdx(line):
        string = line[1:len(line)]
        regnr = int(string)
        regnr = regnr +1 
        return "d"+str(regnr)

class RandomRegisterDValue32(InstructionField):

    def __init__(self, name):
        self.name = name
        
    def getString(self):
        return "#Init a Data Register with a Random 32bit value \n" + "movh %" + self.name + ",hi:" + str(randint(0, 65535)*65536) + "\naddi %"+self.name+",%"+self.name+",lo:"+str(randint(0, 65535))

        
class RandomRegisterEValue64(InstructionField):

    def __init__(self, name):
        name=name.replace("e", "d")
        self.name = name
    def getString(self):
        return "#Init a EData Register with a Random 64bit value \n" + "movh %" + self.name + ",hi:" + str(randint(0, 65535)*65536) + "\naddi %"+self.name+",%"+self.name+",lo:"+str(randint(0, 65535)) + "\nmovh %" + getnextdx(self.name) + ",hi:" + str(randint(0, 65535)*65536) + "\naddi %"+getnextdx(self.name)+",%"+getnextdx(self.name)+",lo:"+str(randint(0, 65535))

class RandomRegisterDPSWRM (InstructionField):

    def __init__(self, name):
        self.name = name
    def getString(self):
        return "#Update PSW with Random Rounding Mode \n" + "movh %" + self.name + ",hi:" + "0" + "\naddi %"+self.name+",%"+self.name+",lo:"+str(randint(0, 3)+3*256) + "\nupdfl %"+self.name

class RandomRegisterDPSWRM_0 (InstructionField):

    def __init__(self, name):
        self.name = name
    def getString(self):
        return "#Update PSW with Random Rounding Mode \n" + "movh %" + self.name + ",hi:" + "0" + "\naddi %"+self.name+",%"+self.name+",lo:"+str(0+3*256) + "\nupdfl %"+self.name

class RandomRegisterDPSWRM_1 (InstructionField):

    def __init__(self, name):
        self.name = name
    def getString(self):
        return "#Update PSW with Random Rounding Mode \n" + "movh %" + self.name + ",hi:" + "0" + "\naddi %"+self.name+",%"+self.name+",lo:"+str(1+3*256) + "\nupdfl %"+self.name

class RandomRegisterDPSWRM_2 (InstructionField):

    def __init__(self, name):
        self.name = name
    def getString(self):
        return "#Update PSW with Random Rounding Mode \n" + "movh %" + self.name + ",hi:" + "0" + "\naddi %"+self.name+",%"+self.name+",lo:"+str(2+3*256) + "\nupdfl %"+self.name

class RandomRegisterDPSWRM_3 (InstructionField):

    def __init__(self, name):
        self.name = name
    def getString(self):
        return "#Update PSW with Random Rounding Mode \n" + "movh %" + self.name + ",hi:" + "0" + "\naddi %"+self.name+",%"+self.name+",lo:"+str(3+3*256) + "\nupdfl %"+self.name

        
class RegisterOffset(InstructionField):

    def __init__(self, name, offset_len, sign):
        self.name = "%" + name
        self.length = (1 << offset_len) -1
        if sign == 1:
            self.start = -(1 << (offset_len-1))
            self.end   =   -(self.start + 1)
        else:
            self.start = 0
            self.end   = self.length

    def getString(self):
        return "["+self.name+"]"+str(randint(self.start/4, self.end /4) << 2)

class RandomRegisterOffset(InstructionField):

    def __init__(self, regtype, offset_len, sign):
        self.regtype = regtype
        self.length = (1 << offset_len) -1
        if sign == 1:
            self.start = -(1 << (offset_len-1))
            self.end   =   -(self.start + 1)
        else:
            self.start = 0
            self.end   = self.length

    def getString(self):
        global baseJumpReg
        r = baseJumpReg
        if self.regtype == "a":
            while r == baseJumpReg or r == baseMemReg:
                r = randint(0,15)
        else:
            r = randint(0,15)
        return "[%"+self.regtype + str(r) +"]"+str(randint(self.start/4, self.end /4) << 2)

class RegisterOffsetIncr(InstructionField):

    def __init__(self, name, offset_len, sign, pre):
        self.name = "%" + name
        self.pre = pre
        self.length = (1 << offset_len) -1
        if sign == 1:
            self.start = -(1 << (offset_len-1))
            self.end   =   -(self.start + 1)
        else:
            self.start = 0
            self.end   = self.length

    def getString(self):
        if self.pre == 1:
            return "[++"+self.name+"]"+str(randint(self.start/4, self.end /4) << 2)
        else:
            return "["+self.name+"++]"+str(randint(self.start/4, self.end /4) << 2)

class RandomRegister(InstructionField):

    def __init__(self, regtype):
        global lastRegister
        self.regtype = regtype

    def getString(self):
        global baseJumpReg
        r = baseJumpReg
        if self.regtype == "a":
            while r == baseJumpReg or r == baseMemReg:
                r = randint(0,15)
        else:
            r = randint(0,15)

        return "%" + self.regtype + str(r)

class RandomRegisterMode(InstructionField):

    def __init__(self, regtype, mode):
        self.regtype = regtype
        self.mode = mode

    def getString(self):
        global baseJumpReg
        r = baseJumpReg
        if self.regtype == "a":
            while r == baseJumpReg or r == baseMemReg:
                r = randint(0,15)
        else:
            r = randint(0,15)

        return "%" + self.regtype + str(r) + self.mode

class RandomRegister64(InstructionField):

        def __init__(self, regtype):
            self.regtype = regtype

        def getString(self):
            r = baseJumpReg
            if self.regtype == "a":
                while r == baseJumpReg or r == baseMemReg:
                    r = randint(0,7) << 1
            else:
                r = randint(0,7) << 1

            return "%" + self.regtype + str(r)

class Constant(InstructionField):

    def __init__(self, val):
        self.name = str(val)


class RandomPosWidthPair(InstructionField):

    def __init__(self, lengthPos, lengthWidth):
        self.lengthPos = (1 << lengthPos) -1
        self.lengthWidth = (1 << lengthWidth) -1

    def getString(self):
        pos = 64
        width = 0
        while (pos + width > 32):
            pos = randint(0, self.lengthPos)
            width = randint(0, self.lengthWidth)
        return str(pos) + ", " + str(width)

class RandomConstant(InstructionField):

    def __init__(self, length, sign):
        self.length = (1 << length) -1
        if sign == 1:
            self.start = -(1 << (length-1))
            self.end   =   -(self.start + 1)
        else:
            self.start = 0
            self.end   = self.length

    def getString(self):
        return str(randint(self.start, self.end))

class RandomAbsConstant(InstructionField):

    def __init__(self):
        self.base = 0xd0000000

    def getString(self):
        return str(self.base)
        return str(self.base + (randint(0, 100) << 2))

class JumpMarker:

    def __init__(self, name):
        self.name = name

    def getString(self):
        return self.name + ":"

class JumpOffset(InstructionField):

    def __init__(self, maxOffset):
        self.maxOffset = maxOffset

    def init(self, currInsn, programLen):
        if (currInsn + self.maxOffset / 2) > programLen -2:
            self.offset = currInsn + 1
        else:
            self.offset = currInsn + randint(1, (self.maxOffset / 2))

    def getString(self):
        global jumpMarkerList

        if self.offset not in jumpMarkerList:
            jumpMarkerList[self.offset] = JumpMarker("label"+str(self.offset))

        return "label"+str(self.offset )


class Instruction:

    insn_fields = list() # generate instruction depending on format.
    name = None

    def __init__(self, n, insn_fields):
        self.name = n
        self.insn_fields = insn_fields

    def get_asm(self):
        result = self.name.strip() + " "
        for field in self.insn_fields:
            result = result + field.getString() + ", "
        return result[0:-2]

    def print_asm(self):
        print_out(self.get_asm())

