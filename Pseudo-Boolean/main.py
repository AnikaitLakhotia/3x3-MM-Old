from encoding import PB
import sys

number_of_multiplications = sys.argv[1]


pb = PB(int(number_of_multiplications))
pb.create_encoding()

# for a,b,y
# 8 aux vars
# each aux var has 8 statements
# thus all 8 vars has 64 statements + 1 for the combiantion of all so 5
