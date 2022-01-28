JOBS=$(shell echo `nproc`)
NUMRUNS=100

help:
	@echo "Usage: make { tests | clean }"

tests: 
	@cd random-insn-test && ./GenerateTests.py $(NUMRUNS)

clean:
	rm -rf random-insn-test/test*

