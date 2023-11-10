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
# streamlining number.
s ?= 4
# streamlining parameter.
sp ?= 0

run:
	@echo "Running the provided Bash script..."
	@./3x3.sh $(op) $(m) $(n) $(p) $(c) $(lo) $(s) $(sp)
	@echo "Script execution complete."
