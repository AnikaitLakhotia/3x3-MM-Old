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
### CNF Encoding:
Usage: make op= m= n= p= c= lo= s0= s1= sp1= s2= sp2= s3= sp3= solver= seed=
Parameters:
  - op (int): Number of 't's. (Must be greater than or equal to 2) Default: 8
  - m (int): Number of rows in the first matrix. (Must be greater than or equal to 1) Default: 2
  - n (int): Number of columns in the first matrix. (Must be greater than or equal to 1) Default: 2
  - p (int): Number of columns in the second matrix. (Must be greater than or equal to 1) Default: 2
  - c (bool): Commutative encoding is used if True and non-commutative if False. Default: False
  - lo (bool): Lexicographical Ordering Constraints are used if True. Default: False
  - s0 (bool): Streamlining 0 is used if True. Default: False
  - s1 (bool): Streamlining 1 is used if True. Default: False
  - sp1 (int): The parameter associated with the streamlining 1. (Must be greater than or equal to {-op * m * n * p} and less than or equal to {op * m * n * p + 1}) Default: -1
  - s2 (bool): Streamlining 2 is used if True. Default: False
  - sp2 (float): The parameter associated with the streamlining 2. (Must be less than or equal to 1.0 and greater than or equal to 0.0) Default: 0.5
  - s3 (bool): Streamlining 3 is used if True. Default: False
  - sp3 (int): The parameter associated with the streamlining 3. ({sp3 + op} must be equal to {m * n * p}) Default: 4
  - seed (None or int): Seed for calls to the random module's functions across the Python codebase. (for repeatability of experiments) Default: None

Note: if any of the parameters are not specified, the default values will be used.

## Supported Solvers
### CNF Encoding
1. MapleSAT
2. CaDiCaL
3. YalSAT
### PB Encoding
1. MapleSAT
2. CaDiCaL
3. RoundingSat

## Directory Structure
---- 3x3-MM\
---- maplesat\
---- cadical\
---- yalsat
