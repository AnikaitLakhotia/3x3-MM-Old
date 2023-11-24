.PHONY: run

# To run the script enter `make run op=8 m=2 n=2 p=2`

# Please clone roundingsat [from here](https://gitlab.com/MIAOresearch/software/roundingsat) and follow the regular build process (non-debug build) in the README.md of roundingsat

# Stucture your directory as follows:
  # ---- 3x3-MM
  # ---- roundingsat

# op = number of multiplications
op ?= 23
# number of rows in matrix A
m ?= 3
# number of cols in matrix A and rows in matrix B
n ?= 3
# number of cols in matrix B
p ?= 3
# streamlining 
s ?= 0


run:
	@./pb.sh $(op) $(m) $(n) $(p) $(s)
