import sys
import time

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
    result = [int(v) for v in result]
    return result


def run_test():
    k = 651056770906015076056810763456358567190100156695615665659
    j = 0
    averageTime = 0
    nist = [651056770906015076056810763456358567190100156695615665659,
            2695995667150639794667015087019625940457807714424391721682712368051,
            115792089210351248362697456949407573528996955234135760342422159061068512044339,
            26959956671506397946670150870196259404578077144243917216827126959956671506397946670150870196259404578077144243917216,
            2695995667150639794667015087019625940457807714424391721682712368058238947189273490172349807129834790127349087129834623486127461012630462184628923461201280461]
    w = [5, 7, 9 , 11]
    index_w = 0
    index_nist = 0
    while index_w < 1:
        while index_nist < 5:
            while j < 1000:
                j = j+1
                startTime = time.time()
                l_naf = find_naf(nist[index_nist], 2, w[index_w])
                # print l_naf
                endTime = time.time()
                averageTime = averageTime + (endTime - startTime)
            averageTime = averageTime / 1000
            # print "rdr = ", rdr, " Min Length = ", min_length, " Average Time for digit set of Size ", i, " = ", averageTime
            print "Average Time wNAF of window ", w[index_w], " for NIST [", index_nist, "] = ", averageTime
            averageTime = 0
            j = 0
            index_nist = index_nist +1
        index_nist = 0
        index_w = index_w + 1

if __name__ == '__main__':
    run_test()
    # x = find_naf(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]));
    # x.reverse()
    # print x
    # print bin(int(sys.argv[1]))
