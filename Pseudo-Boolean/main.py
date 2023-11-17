from encoding import PB
import sys

_, number_of_multiplications, m, n, p = sys.argv

pb = PB(int(number_of_multiplications), int(m), int(n), int(p))
pb.create_encoding()
pb.opb_file.close()
