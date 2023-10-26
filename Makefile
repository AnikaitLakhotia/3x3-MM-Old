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

run:
	@echo "Running the provided Bash script..."
	@./3x3.sh $(op) $(m) $(n) $(p)
	@echo "Script execution complete."
