# Matrix Multiplication PB and CNF Encoding Pipeline

## Objective
The goal of developing the Matrix Multiplication Pipeline is to establish an end-to-end process capable of generating a pseudo-boolean (PB) or canonical normal form (CNF) encoding for the multiplication of any two matrices. The first matrix has dimensions mxn, and the second matrix has dimensions nxp. This encoding adheres to a specified number of scalar multiplications, as defined by the Brent equations.

## Pipeline Process
The pipeline operates by accepting input parameters such as matrix sizes and the required number of scalar multiplications for the matrix scheme. It then processes this information through a supported solver, determining the existence of a multiplication scheme. If a scheme is identified, the assigned variables undergo verification against the Brent equations. Additionally, the scheme is subjected to validation against the naive matrix multiplication method using 100 randomly generated matrices.

## PB Encoding Pipeline
The PB pipeline also supports converting the PB constraints to CNF, allowing the use of state-of-the-art SAT solvers. Currently, two translators are supported:
1. MiniSat+
2. PBLib

## How to use
This needs to be updated. We should have one makefile which can run the PB and CNF pipeline. 

## Supported Solvers
### CNF Encoding
1. MapleSAT
2. CaDiCaL
### PB Encoding
1. MapleSAT
2. CaDiCaL
3. RoundingSat
