.PHONY: clean run_script
run_script:
	@echo "Running the provided Bash script..."
	@./3x3.sh
	@echo "Script execution complete."

clean:
	@echo "Removing all .txt, .cnf and .drat files..."
	@rm -f *.txt *.cnf *.drat
	@echo "Done."

