# -*- coding:utf-8 -*-
from numpy import int32

def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint: 
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1 
    return val


def ansii(a):
    return a.encode('gbk')


def kr(a:int, b):
    c = 0
    b = ansii(b)
    while c < len(b)-2:
        d = b[c + 2]
        d = d - 87 if ansii("a")[0] <= d else int(chr(d))
        d = a >> d if ansii("+")[0] == b[c + 1] else a << d
        d = int_overflow(d)
        a = a + d & 4294967295 if ansii("+")[0] == b[c] else a ^ d
        c += 3
    return int_overflow(a)

def mr(q, TKK):
    e = q.encode()
    d = str(TKK).split('.')
    a = int(d[0])
    b = int(d[0])

    for f in e:
        a += f
        a = kr(a, "+-a^+6")
    a = kr(a, "+-3^+b+-f")
    a &= 0xffffffff # 出错了，转回无符号
    a ^= (int(d[1]) or 0)
    if 0 > a:
        a = (a & 2147483647) + 2147483648
    a %= 1E6
    a = int(a)

    # c = '&tk='
    # return c + (str(a) + "." + str(a ^ b))
    return (str(a) + "." + str(a ^ b))


"""
def Sr(a, TKK):
    a = ''.join(a['a']['b']['q'])
    return mr(a, TKK)
d = {
    'a':{
        'a': ['q'],
        'b': {
            'q': ['me']
        },
        'c': 1,
        'g': 1
    },
    'b': 1,
    'c': None,
    'j': False,
}
TKK = '426151.3141811846'
tk = Sr(d, TKK)
print(tk)
"""