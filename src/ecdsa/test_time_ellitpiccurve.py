from ellipticcurve import CurveFp, INFINITY, Point
from six import print_
import time
import revisited_rdr

def test_ellipticcurve():
  class FailedTest(Exception):
    pass
    
  # NIST Curve P-192:
  p = 6277101735386680763835789423207666416083908700390324961279
  r = 6277101735386680763835789423176059013767194773182842284081
  # s = 0x3045ae6fc8422f64ed579528d38120eae12196d5L
  c = 0x3099d2bbbfcb2538542dcd5fb078b6ef5f3d6fe2c745de65
  b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
  Gx = 0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012
  Gy = 0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811

  c192 = CurveFp(p, -3, b)
  p192 = Point(c192, Gx, Gy, r)

  # Checking againtest_doublest some sample computations presented
  # in X9.62:
  digt_set = [1, 23, 27, 43, 47, 49, 53, 57, 69, 95, 103, 113, 117, 129, 153, 155, 171, 173, 175, 187, 191, 199, 213, 215, 239, 247, 271, 275, 281, 297, 303, 315, 321, 327, 339, 349, 369, 383, 391]
  RDR = [53, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 0, 0, -153, 0, 0, 0, 0, 0, 0, -95, 0, 0, 0, 0, 0, -95, 0, 0, 0, 0, 0, 0, 0, 0, -175, 0, 0, 0, 0, 349, 0, 0, 0, 0, 0, 69, 0, 0, 0, 0, 0, 187, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, -349, 0, 0, 0, 0, 0, -95, 0, 0, 0, 0, 0, 27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -213, 0, 0, 0, 0, 0, 0, 0, 327, 0, 0, 0, 0, 0, 0, -349, 0, 0, 0, 0, 0, 0, 0, 0, 187, 0, 0, 0, 0, 0, 0,0, 0, -57, 0, 0, 0, 0, 0, 0, 297, 0, 0, 0, 0, 0, 0, 339, 0, 0, 0, 0, 0, 0, 0, -391, 0, 0, 0, 0, 0, 0, -391, 0, 0, 0, 0, 0, 0, -391, 0, 0,0, 0, 0, -247, 0, 0, 0, 0, 0, 0, 0, 0, -43, 0, 0, 0, 0, 0, 187]
  naf= [1, 0, -1, 0, 1, 0, 1, 0, 0, 1, 0, 0, -1, 0, -1, 0, -1, 0, -1, 0, 1, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, -1, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0,-1, 0, 0, 0, 1, 0, -1, 0, 0, -1, 0, -1, 0, 0, -1, 0, 1, 0, -1, 0, -1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, -1, 0, 0, 1, 0, 1, 0, -1, 0, -1, 0, -1, 0, 0, -1, 0, 1, 0, 0, 1, 0, -1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, -1, 0, -1, 0, 0, 0, -1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, -1, 0, -1]
  d = 651056770906015076056810763456358567190100156695615665659
  i = 1000

  doubleadd_time = 0
  naf_time = 0
  rdr_time = 0
  while (i > 0):
    print i
    startTime = time.time()
    Q = d * p192
    endTime = time.time()
    doubleadd_time = doubleadd_time + (endTime - startTime)
    # print("Double and add > ", endTime - startTime)

    startTime = time.time()
    G = p192.RDR_multiply_index(digt_set, RDR, i)
    endTime = time.time()
    rdr_time = rdr_time + (endTime - startTime)
    # print("RDR > ", endTime - startTime)

    startTime = time.time()
    N = p192.NAF_multiply(naf)
    endTime = time.time()
    naf_time = naf_time + (endTime - startTime)
    # print("NAF > ", endTime - startTime)
    i = i - 1

  print ("Double and Add average > ", doubleadd_time/1000)
  print ("RDR average > ", rdr_time/1000)
  print ("NAF average > ", naf_time/1000)

  print("N > ", N.y())
  print("X > ", G.y())
  print("Q > ", Q.y())
  if Q.x() != 0x62B12D60690CDCF330BABAB6E69763B471F994DD702D16A5:
    raise FailedTest("p192 * d came out wrong.")
  else:
    print_("p192 * d came out right.")

  k = 6140507067065001063065065565667405560006161556565665656654
  R = k * p192
  if R.x() != 0x885052380FF147B734C330C43D39B2C4A89F29B0F749FEAD \
     or R.y() != 0x9CF9FA1CBEFEFB917747A3BB29C072B9289C2547884FD835:
    raise FailedTest("k * p192 came out wrong.")
  else:
    print_("k * p192 came out right.")

  u1 = 2563697409189434185194736134579731015366492496392189760599
  u2 = 6266643813348617967186477710235785849136406323338782220568
  temp = u1 * p192 + u2 * Q
  if temp.x() != 0x885052380FF147B734C330C43D39B2C4A89F29B0F749FEAD \
     or temp.y() != 0x9CF9FA1CBEFEFB917747A3BB29C072B9289C2547884FD835:
    raise FailedTest("u1 * p192 + u2 * Q came out wrong.")
  else:
    print_("u1 * p192 + u2 * Q came out right.")

  # NIST Curve P-192:
  p = 26959946667150639794667015087019630673557916260026308143510066298881
  n = 26959946667150639794667015087019625940457807714424391721682722368061
  #SEED = bd713447 99d5c7fc dc45b59f a3b9ab8f 6a948bc5
  c = 0x5b056c7e11dd68f40469ee7f3c7a7d74f7d121116506d031218291fb
  b = 0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4
  Gx = 0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21
  Gy = 0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34


  # NSIT Curve P-256
  p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
  n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
  #SEED = 0xc49d360886e704936a6678e1139d26b7819f7e90
  c = 0x7efba1662985be9403cb055c75d4f7e0ce8d84a9c5114abcaf3177680104fa0d
  b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
  Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
  Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5

  # NIST Curve P-384
  p = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319
  n = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
  # SEED = 0xa335926aa319a27a1d00896a6773a4827acdac73
  c = 0x79d1e655f868f02fff48dcdee14151ddb80643c1406d0ca10dfe6fc52009540a495e8042ea5f744f6e184667cc722483
  b = 0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef
  Gx = 0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7
  Gy = 0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f

  # NIST Curve P-521
  p = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
  n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449
  # SEED = 0xd09e8800291cb85396cc6717393284aaa0da64ba
  c = 0x0b48bfa5f420a34949539d2bdfc264eeeeb077688e44fbf0ad8f6d0edb37bd6b533281000518e19f1b9ffbe0fe9ed8a3c2200b8f875e523868c70c1e5bf55bad637
  b = 0x051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00
  Gx = 0xc6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66
  Gy = 0x11839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650



if __name__ == "__main__":
  test_ellipticcurve();