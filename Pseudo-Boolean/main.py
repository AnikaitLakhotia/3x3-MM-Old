from encoding import PB
import sys

number_of_multiplications = sys.argv[1]


pb = PB(int(number_of_multiplications))
pb.create_encoding()
