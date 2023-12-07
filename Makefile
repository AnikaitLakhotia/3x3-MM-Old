.PHONY: clean run_script

# stucture your directory as follows:
  # ---- 3x3-MM
  # ---- cadical
  # ---- drat-trim

# op = number of multiplications
op ?= 8
# number of rows in matrix A
m ?= 2
# number of cols in matrix A and rows in matrix B
n ?= 2
# number of cols in matrix B
p ?= 2
# Indicates whether to use commutative encoding.
c ?= False
# Indicates whether to use lex ordering.
lo ?= False
# Indicates whether to use streamlining 0.
s0 ?= False
# Indicates whether to use streamlining 1.
s1 ?= False
# streamlining 1 parameter.
sp1 ?= -1
# Indicates whether to use streamlining 2.
s2 ?= False
# streamlining 2 parameter.
sp2 ?= 0.5
# Indicates whether to use streamlining 3.
s3 ?= False
# streamlining 3 parameter.
sp3 ?= 4
# SAT solver
solver ?= cadical
# Seed for random() function
seed ?= None

run:
	@echo "Running the provided Bash script..."
	@./3x3.sh $(op) $(m) $(n) $(p) $(c) $(lo) $(s0) $(s1) $(sp1) $(s2) $(sp2) $(s3) $(sp3) $(solver) $(seed)
	@echo "Script execution complete."
