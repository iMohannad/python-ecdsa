import math
import random
import sys
import time

""" Convert integer k to NAF format using the following algorithm
    i <- 0
    while k > 0 do
       if k is odd then
           zi <- 2 - (k mod 4)
           k <- k - zi
       else
           zi <- 0
       k <- k/2
       i <- i + 1
   return z
"""
def convertNAF(k):
    naf = [];
    while k > 0:
        if (k%2 == 0):
            naf.insert(0, 0);
        else:
            zi = 2 - (k % 4);
            naf.insert(0, zi);
            k = k - zi;
        k = k/2;
    return naf;

""" An array of a number is passed to the function,
    The function determines if the number is a NAF number or not
    Which means that there is no two consecutive  1s in the array """
def isNAF(naf):
    length = len(naf);
    i = 0;
    while i < length - 1:
        if (naf[i] == 1 and naf[i] == naf[i+1]):
            return False;
        i += 1;
    return True;

""" convert integer k to its binary representation """
def convertBinary(k):
    binNum = []
    while k > 0:
        binNum.insert(0, k % 2);
        k = k/2;
    return binNum

"""
    wmax(k) is the largest integer w <= WMAX such that two conditions are satisified:
    1. di < k,
    2. pw(k) in Dw'

    Parameters
    ----------
    k : int
        an integer k to be represented in random representation
    WMAX : int
        WMAX is the integer calculate from get_WMAX(D)

    Returns
    -------
    int
        an integer that satisifies the two coniditons for wmax(k)
"""
def wmax(k, Wn, D):
    w = Wn + 2;
    for i in range(Wn + 2, 1, -1):
        d_flag = False;
        D_neg = get_D_neg(D, i);
        D_pos = get_D_pos(D, i);
        # print "------------ WMAX = ", i, " ----------------"
        # print "D_pos_", i, " = ", D_pos
        # print "D_neg_", i, " = ", D_neg

        # check the first candidate where di \in D < k
        for d in D:
            if d < k:
                if (pw(k, i) == pw(d, i)):
                    return i;
                if (pw(k, i) == 2**i - pw(d, i)):
                    return i;

        # print "--------------------------------------------"
    return w;



# pw(k) = k % (2**w)
def pw(k, w):
    if (k < 0):
        return k + (2**w);
    return k % (2**w);

"""
    Calculcate the set D_w

    Parameters
    ----------
    arg1 : List
        set of odd integers
    arg2 : int
        an integer >= 2

    Returns
    -------
    List
        a list that contains Dw which is pw(d) for each d in D
"""
def get_D_pos(D, w):
    D_pos = [];
    for d in D:
        entry = pw(d, w)
        if (entry not in D_pos):
            D_pos.append(entry)
    D_pos.sort();
    return D_pos;


def get_D_pos_k(D, w, k):
    D_pos = [];
    for d in D:
        if (d > k):
            break;
        entry = pw(d, w)
        if (entry not in D_pos):
            D_pos.append(entry)
    D_pos.sort();
    return D_pos;
"""
    Calculcate the set D_w' by using Dw

    Parameters
    ----------
    arg1 : List
        set of odd integers
    arg2 : int
        an integer >= 2

    Returns
    -------
    List
        a list that contains Dw and Dw_Neg
"""
def get_D_neg(D, w):
    D_pos = get_D_pos(D, w);
    Dw_Neg = [];
    const = 2**w;
    for d in D_pos:
        Dw_Neg.append(const - d);

    Dw_Neg.sort();
    return Dw_Neg;

def get_D_neg_k(D, w, k):
    D_pos = get_D_pos_k(D, w, k);
    Dw_Neg = [];
    const = 2**w;
    for d in D_pos:
        Dw_Neg.append(const - d);

    Dw_Neg.sort();
    return Dw_Neg;

# Get the union of D+ and D-
def get_Dw(D, w):
    D_pos = get_D_pos(D, w);
    D_neg = get_D_neg(D, w);
    result = list(set().union(D_pos, D_neg));
    result.sort();
    return result;

def get_Wn(D):
    return int(math.floor(math.log(max(D), 2)));

def digitD(k, D):
    if k % 2 == 0:
        return 0;
    if k == 1:
        return k;
    Wn = get_Wn(D);
    h = wmax(k, Wn, D);
    D_pos = get_D_pos_k(D, h, k);
    D_neg = get_D_neg_k(D, h, k);
    # print "---------------------";
    # print "k = ", k, " h = ", h
    # print "D_pos = ", D_pos
    # print "D_neg = ", D_neg;
    result = -100;
    flag_cond1 = False;
    if pw(k, h) in D_pos:
        for d in D:
            # if d >= k:
            #     continue;
            # print "pw(k, h) > ", pw(k, h), "pw(", d, ", h) > ", pw(d, h)
            if pw(k, h) == pw(d, h):
                # print "Result > ", d;
                result = d;
                break;
    else:
        # print "2**h - pw(", k, ", h) > ", (2**h - pw(k, h))
        for d in D:
            # if d >= k:
            #     continue;
            # print "pw(k, h) > ", pw(k, h), "2**h - pw(d, h) > ", (2**h - pw(d, h))
            if pw(k, h) == (2**h - pw(d, h)):
                # print "Result > ", d;
                result = -d;
                break;

    # print "---------------------";
    return result;
    # print Wmax
    # print Dwmax
    # print "2**Wmax ", 2**Wmax
    # print "pw(k, Wmax) ", pw(k, Wmax)
    # print "2**Wmax - pw(k, Wmax = ", 2**Wmax - pw(k, Wmax)
    # print "no condition"


def RDP(k, D):
    bin_k = []; # binary representation of k to contain the result
    while k != 0:
        ki = digitD(k, D);
        bin_k.insert(0, ki);
        k = (k - ki) / 2;
        # print "k > ", k

    return bin_k;


def generate_random_D(m, l):
    if l > (m+1)/2:
        raise ValueError("l should satisfy the condition l <= (m+1)/2");
    D = [];
    for i in range(2, l+1, 1):
        odd = False;
        while not odd:
            x = random.randint(3, m);
            if(x % 2 != 0 and x not in D):
                odd = True;
        D.append(x);
    D.sort();
    return D;

""" To run the program, you need to input 3 values,
    k: The number to be converted
    m: it's an upper bound for the set of numbers where the set D will be generated from
       so, if m = 10 it means, D will be generated from the set [1, 2 .... 10]
    l: The number of elements in the set D.

    Running the program from a terminal as follows:
    python recording_alg.py k m l   (Where k, m, and l are numbers)
"""
def RDR(m, l, k):
    D = generate_random_D(m, l);
    #D = [3, 23, 27, 53, 61, 71, 79, 97]
    D.insert(0, 1)
    #print "D > ", D
    result = RDP(k, D)
    naf = convertNAF(k)
    #print "Length of RDR = ", len(result)
    #print "Length of NAF = ", len(naf)
    #print "k = ", k, "\nRDR = ", result, "\tLength > ", len(result)
    #print "NAF = ", naf , "Length > ", len(naf) #, "\t\tLength -> ", len(result);
    # print "Length => ", len(result)
    return [D, result, naf, len(result)]

def run_tests_time():
    i = 5
    [D, Di, naf, min_length] = RDR(1000, i, 26959956671506397946670150870196259404578077144243917216827126959956671506397946670150870196259404578077144243917216)
    min_len = min_length
    D_set = D
    D_result = Di
    naf_result = naf
    j = 0
    averageTime = 0
    while i <= 300:
        while j < 1000:
            startTime = time.time()
            [D, Di, naf, min_length] = RDR(1000, i, 269599566715063979466701508701962594045780726959956671506397946670150870196259404578077144243917216827126959956671506397946670150870196259404578077144243917216714424391721682712368051)
            endTime = time.time()
            averageTime = averageTime + (endTime - startTime)
            j = j+1
        averageTime = averageTime / 1000
        print "Average Time for digit set of Size ", i, " = ", averageTime
        averageTime = 0
        j = 0
        i = i+1


if __name__ == "__main__":
    time_flag = 0
    if time_flag:
        run_tests_time()
    else:
        i = 10
        [D, Di, naf, min_length] = RDR(1000, i, 26959956671506397946670150870196259404578077144243917216827126959956671506397946670150870196259404578077144243917216)
        min_len = min_length
        D_set = D
        D_result = Di
        naf_result = naf
        while i <= 300:
            [D, Di, naf, min_length] = RDR(1000, i, 26959956671506397946670150870196259404578077144243917216827126959956671506397946670150870196259404578077144243917216)
            if min_length < min_len :
                D_set = D
                D_result = Di
                naf_result = naf
            i = i+1

        print "D = ", D_set
        print  "RDR = ", D_result, "\tLength > ", len(D_result)
        print "NAF = ", naf_result , "Length > ", len(naf_result)