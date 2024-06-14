.PHONY: run

# To run the script enter `make run op=8 m=2 n=2 p=2`

# Please clone roundingsat [from here](https://gitlab.com/MIAOresearch/software/roundingsat) and follow the regular build process (non-debug build) in the README.md of roundingsat

# Structure your directory as follows:
# ---- 3x3-MM
#   ---- Pseudo-Boolean
#   ---- minisat+
#   ---- pblib
#   ---- drat-trim
#   ---- cadical

# op = number of multiplications
op ?= 4
# number of rows in matrix A
m ?= 1
# number of cols in matrix A and rows in matrix B
n ?= 2
# number of cols in matrix B
p ?= 2
# streamlining 
s ?= 0
# percentage of changes from streamlining
c ?= 0
# translator library: 0. no translator (instance is solved with roundingsat), 1. minisat+, 2. pblib
t ?= 2
# encoding type: 0. naive, 1. optimized
e ?= 0
# expirement identifier
id ?= 0

run:
	@./pb.sh $(op) $(m) $(n) $(p) $(s) $(c) $(t) $(e) $(id)
