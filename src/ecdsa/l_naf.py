import sys


def find_naf(k, l, w):
    i = 0
    ki = -7
    result = []
    while k > 0:
        if (k % l) != 0:
            ki = k % (l**w)
            if ki > ((l**w)/2):
                ki = ki - (l**w)
            k = k - ki
        else:
            ki = 0
        k = k/l
        result.append(ki)
    result.reverse()
    return result



if __name__ == '__main__':
    x = find_naf(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]));
    x.reverse()
    print x
    print bin(int(sys.argv[1]))
