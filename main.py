from encoding import encoding
from verifier import verifier
if __name__ == '__main__':
    encoding, cumulative_dict = encoding(18, 3)
    print(encoding)
    cumulative_string = ""
    print(verifier(cumulative_string, cumulative_dict, 18))
