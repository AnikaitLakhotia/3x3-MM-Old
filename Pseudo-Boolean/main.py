from encoding import NaiveEncoding, OptimizedEncoding
import sys

_, number_of_multiplications, m, n, p, s, c, translator_type, encoding_type, id = sys.argv
pb = 0
if encoding_type == "0":
    pb = NaiveEncoding(int(number_of_multiplications), int(
    m), int(n), int(p), int(s), int(c), int(translator_type), int(encoding_type), id)
elif encoding_type == "1":
    pb = OptimizedEncoding(int(number_of_multiplications), int(
    m), int(n), int(p), int(s), int(c), int(translator_type), int(encoding_type), id)

pb.create_encoding()
pb.opb_file.close()
