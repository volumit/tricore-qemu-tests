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

import os, sys
from random import randint
import argparse

from Config import *
from TestCase import TestCase


def cleanup():
    print "No Clean up, do it with make ..."
#    os.system("rm -r test*")

def main():

    parser = argparse.ArgumentParser(description='TriCore random test generator')
    parser.add_argument('-q', help="Quiet mode", action='store_true')
    parser.add_argument('runs', type=int, help='Number of tests to run')
    args = parser.parse_args()

    print os.getcwd()
    fails = list()

    for i in range(1, args.runs + 1):
        case1 = TestCase("test"+str(i), randint(1, maxInsnPerTest))
        case1.compile()
        case1.runTSIM()
        case1.runQEMU()
        case1.compareResults()
        if case1.evaluateSucess() == 0:
            fails.append(case1.name)

    if not fails:
        print "All test sucessfull"
        cleanup()

    for fail in fails:
        print fail + " failed"
main()
