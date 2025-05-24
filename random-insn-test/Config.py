############################
##
##  Config
##
###########################
#prefix = "/home/dummy/tricore_494_linux/bin/"
#tc18
prefix = "/home/dummy/tricore_113_linux/bin/"

tas     = prefix + "tricore-elf-as"
#tas_flags ="-mtc162 -o0"
#tc18
tas_flags ="-mtc18 -o0"

tld     = prefix + "tricore-elf-ld"
#tld_flags = "--mcpu=tc162 -T target.ld "
#tc18
tld_flags = "--mcpu=tc18 -T target.ld "

tobjdump     = prefix + "tricore-elf-objdump"
tobjdump_flags = "-D "

#tsim = "/home/dummy/BUILD/build_linux_gcc494/testsuite/gcc/tsim16p_e"
#tsim_flags = "-DConfig ../DCONFIG -MConfig ../MCONFIG -e -disable-watchdog -x 100000 -o "
#tsim_flags = "-tc162p -DConfig ../DCONFIG -MConfig ../MCONFIG -e -disable-watchdog -x 100000 -o "

#for tc18
tsim = "/home/dummy/BUILD/build_linux_gcc940/testsuite_gcc940/gcc/tsim16p_e_mtc18"
#tsim_flags = "-DConfig ../DCONFIG -MConfig ../MCONFIG -e -disable-watchdog -x 100000 -o "
tsim_flags = "-tc18 -dp_fpu -DConfig ../DCONFIG -MConfig ../MCONFIG -e -disable-watchdog -x 100000 -o "

#qemu = "/home/dummy/qemu_tricore_6250/bin/qemu-system-tricore"
#qemu_flags = " -M tricore_tsim162 -display none -singlestep -D qemu.result -d nochain,exec,cpu "
#qemu_flags = " -M tricore_tsim162 -nographic -singlestep -D qemu.result -d nochain,exec,cpu "
#for tc18
qemu = "/home/dummy/qemu_tricore_6250_tc18/bin/qemu-system-tricore"
#qemu_flags = " -M tricore_tsim162 -display none -singlestep -D qemu.result -d nochain,exec,cpu "
qemu_flags = " -M tricore_tsim18 -nographic -singlestep -D qemu.result -d nochain,exec,cpu "

baseJumpReg = 14
baseMemReg = 15

maxInsnPerTest = 2000

