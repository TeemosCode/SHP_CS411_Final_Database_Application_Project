# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:41:18 2016

@author: lcl
"""
import math
#Max number = 10^16 - 2 = 9999999999999998
#               2^53     = 9007199254740992
biRadixBase = 2
biRadixBits = 16
bitsPerDigit = biRadixBits
biRadix = 1 << 16
biHalfRadix = biRadix >> 1  #原为 >>> ，代表无符号右移位
biRadixSquared = biRadix * biRadix
maxDigitVal = biRadix - 1
maxInteger = 9999999999999998

maxDigits = None
ZERO_ARRAY = None
bigZero = None
bigOne = None

class BigInt:
    isNeg = False
    digits = None
    def __init__(self,flag):
        #global ZERO_ARRAY
        if ((type(flag) == type(True)) and (flag == True)):
            self.digits = None
        else:
            self.digits = [0] * 129 #--Change 20 to 19--#
        self.isNeg = False

def setMaxDigits(value):
    global ZERO_ARRAY,bigZero,bigOne,maxDigits
    maxDigits = value
    ZERO_ARRAY = []
    for iza in range(maxDigits):
        ZERO_ARRAY.append(0)
    
    bigZero = BigInt(False)
    bigOne = BigInt(False)
    bigOne.digits[0] = 1

setMaxDigits(129)    #--Change 20 to 19--#

dpl10 = 15
def biFromNumber(i):
    global biRadixBits,maxDigitVal
    result = BigInt(False)
    result.isNeg = (i < 0)
    i = abs(i)
    j = 0
    while (i > 0):
        result.digits[j] = i & maxDigitVal
        j += 1
        i >>= biRadixBits
    return result
lr10 = biFromNumber(1000000000000000)

def biFromDecimal(s):
    isNeg = (s[0] == '-')
    if (isNeg):
        i = 1
    else:
        i = 0
    result = None
    #Skip leading zeros.
    while (i < len(s) and s[i] == '0'):
        i += 1
    if (i == len(s)):
        result = BigInt(False)
    else:
        digitCount = len(s) - i
        fgl = digitCount % dpl10
        if (fgl == 0):
            fgl = dpl10
        result = biFromNumber(int(s[i:i + fgl]))
        i += fgl
        while (i < len(s)):
            result = biAdd(biMultiply(result, lr10),biFromNumber(int(s[i:i + dpl10])))
            i += dpl10
        result.isNeg = isNeg
	return result;

def biCopy(bi):
    result = BigInt(True)
    result.digits = bi.digits
    result.isNeg = bi.isNeg
    return result
    
def reverseStr(s):
    result = ""
    i = len(s) - 1
    while (i > -1):
        result += s[i]
        i -= 1
	return result

hexatrigesimalToChar = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z']

def biToString(x, radix):
    global bigZero
    # 2 <= radix <= 36
    b = BigInt(False)
    b.digits[0] = radix
    qr = biDivideModulo(x, b)
    result = hexatrigesimalToChar[qr[1].digits[0]]
    while (biCompare(qr[0], bigZero) == 1):
        qr = biDivideModulo(qr[0], b)
        digit = qr[1].digits[0]
        #result += hexatrigesimalToChar[qr[1].digits[0]]
        result += hexatrigesimalToChar[digit]
    if (x.isNeg):
        temp = "-"
    else:
        temp = ""
    
    return temp + reverseStr(result)

def biToDecimal(x):
    global bigZero
    b = BigInt(False)
    b.digits[0] = 10
    qr = biDivideModulo(x, b)
    result = str(qr[1].digits[0])
    while (biCompare(qr[0], bigZero) == 1):
        qr = biDivideModulo(qr[0], b)
        result += str(qr[1].digits[0])
    if (x.isNeg):
        temp = "-"
    else:
        temp = ""
    return temp + reverseStr(result)

hexToChar = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','a', 'b', 'c', 'd', 'e', 'f']
"""
def digitToHex(n):
    mask = 0xf
    result = ""
    for i in range(0,4):
        result += hexToChar[n & mask]
        n >>= 4     #原为无符号右移>>>
    return reverseStr(result)
    
def biToHex(x):
    result = ""
    #n = biHighIndex(x)
    i = biHighIndex(x)
    while (i > -1):
        result += digitToHex(x.digits[i])
        print "result from biToHex: ",result
        i -= 1
    return result
"""
def biToHex(x):
    result = []
    temp = []
    for dig in x.digits:
        h = hex(dig)[2:]
        if (h[-1] == 'L'):
            h = h[:-1]
        temp.append(h)    #--hex() return like '0x...'
    
    for i in range(len(temp)-1,-1,-1):
        if (temp[i][0] != '0'):
            if (len(temp[i]) < 4):
                result.append(('0' * (4 - len(temp[i]))) + temp[i])
            else:
                result.append(temp[i])
    
    result = "".join(result)
    return result
    
def charToHex(c):
    ZERO = 48
    NINE = ZERO + 9
    littleA = 97
    littleZ = littleA + 25
    bigA = 65
    bigZ = 65 + 25
    result = None

    if (c >= ZERO and c <= NINE):
        result = c - ZERO
    elif (c >= bigA and c <= bigZ):
        result = 10 + c - bigA
    elif (c >= littleA and c <= littleZ):
        result = 10 + c - littleA
    else:
        result = 0
    return result

def hexToDigit(s):
    result = 0
    sl = min(len(s), 4)
    for i in range(0,sl):
        result <<= 4
        result |= charToHex(ord(s[i]))
    
    return result;

def biFromHex(s):
    result = BigInt(False)
    sl = len(s)
    i = sl
    j = 0
    
    while (i > 0):
        result.digits[j] = hexToDigit(s[max(i - 4, 0):max(i - 4, 0) + min(i, 4)])
        i -= 4
        j += 1
    
    return result

def biFromString(s, radix):
    isNeg = s[0] == '-'
    if (isNeg):
        istop = 1
    else:
        istop = 0
    result = BigInt(False)
    place = BigInt(False)
    place.digits[0] = 1    # radix^0
    i = len(s) - 1
    while (i >= istop):
        c = ord(s[i])
        digit = charToHex(c)
        biDigit = biMultiplyDigit(place, digit)
        result = biAdd(result, biDigit)
        place = biMultiplyDigit(place, radix)
        i -= 1
    result.isNeg = isNeg
    return result

def biToBytes(x):
    #// Returns a string containing raw bytes.
    result = ""
    i = biHighIndex(x)
    while (i > -1):
        result += digitToBytes(x.digits[i])
        i -= 1
        return result

def digitToBytes(n):
    # Convert two-byte digit to string containing both bytes.
    c1 = chr(n & 0xff)
    n >>= 8    #原为无符后右移>>>
    c2 = chr(n & 0xff)
    return c2 + c1

def biDump(b):
    if (b.isNeg):
        temp1 = "-"
    else:
        temp1 = ""
    for i in range(len(b.digits)):
        b.digits[i] = str(b.digits[i])
    temp2 = "".join(b.digits)
    return temp1 + temp2

def biAdd(x, y):
    global biRadix
    result = None
    if (x.isNeg != y.isNeg):
        y.isNeg = not y.isNeg
        result = biSubtract(x, y)
        y.isNeg = not y.isNeg
    else:
        result = BigInt(False)
        c = 0
        n = None
        for i in range(len(x.digits)):
            n = x.digits[i] + y.digits[i] + c
            result.digits[i] = n & 0xffff
            if (n >= biRadix):
                c = 1
            else:
                c = 0
        result.isNeg = x.isNeg
    return result

def biSubtract(x, y):
    global biRadix
    result = None
    if (x.isNeg != y.isNeg):
        #print "test 1"
        y.isNeg = not y.isNeg
        result = biAdd(x, y)
        y.isNeg = not y.isNeg
    else:
        #print "test 2"
        result = BigInt(False)
        n = None
        c = 0
        for i in range(len(x.digits)):
            n = x.digits[i] - y.digits[i] + c
            #print "n=",n," c= ",c
            result.digits[i] = n & 0xffff
            #print i," -> ",result.digits[i]
            # Stupid non-conforming modulus operation.
            if (result.digits[i] < 0):
                result.digits[i] += biRadix
            if (n < 0):
                c = -1
            else:
                c = 0
        
        # Fix up the negative sign, if any.
        if (c == -1):
            c = 0
            for i in range(len(x.digits)):
                n = 0 - result.digits[i] + c
                result.digits[i] = n & 0xffff
                # Stupid non-conforming modulus operation.
                if (result.digits[i] < 0):
                    result.digits[i] += biRadix
                if (n < 0):
                    c = -1
                else:
                    c = 0
            # Result is opposite sign of arguments.
            result.isNeg = not x.isNeg
        else:
            # Result is same sign.
            result.isNeg = x.isNeg
    return result

def biHighIndex(x):
    result = len(x.digits) - 1
    while (result > 0 and x.digits[result] == 0):
        result -= 1
    return result

def biNumBits(x):
    global bitsPerDigit
    n = biHighIndex(x)
    d = x.digits[n]
    m = (n + 1) * bitsPerDigit
    result = m
    while (result > m - bitsPerDigit):
        if ((d & 0x8000) != 0):
            break
        d <<= 1
        result -= 1
    return result

def biMultiply(x, y):
    global biRadixBits,maxDigitVal
    result = BigInt(False)
    c = None
    n = biHighIndex(x)
    t = biHighIndex(y)
    #u = None
    uv = None
    k = None
    
    for i in range(0,t+1):
        c = 0
        k = i
        for j in range(0,n+1):
            uv = result.digits[k] + x.digits[j] * y.digits[i] + c
            result.digits[k] = uv & maxDigitVal
            c = uv >> biRadixBits      #原为无符号右移>>>
            k += 1
        result.digits[i + n + 1] = c
    #Someone give me a logical xor, please.
    result.isNeg = x.isNeg != y.isNeg
    return result

def biMultiplyDigit(x, y):
    global biRadixBits,maxDigitVal
    result = BigInt(False)
    n = biHighIndex(x)
    c = 0
    for j in range(0,n+1):
        uv = result.digits[j] + x.digits[j] * y + c
        result.digits[j] = uv & maxDigitVal
        c = uv >> biRadixBits       #原为无符号右移>>>
    result.digits[1 + n] = c
    return result

def arrayCopy(src, srcStart, dest, destStart, n):
    m = min(srcStart + n, len(src))
    i = srcStart
    j = destStart
    while (i < m):
        dest[j] = src[i]
        i += 1
        j += 1

highBitMasks = [0x0000, 0x8000, 0xC000, 0xE000, 0xF000, 0xF800,0xFC00, 0xFE00, 0xFF00, 0xFF80, 0xFFC0, 0xFFE0,0xFFF0, 0xFFF8, 0xFFFC, 0xFFFE, 0xFFFF]

def biShiftLeft(x, n):
    global bitsPerDigit,maxDigitVal
    digitCount = int(math.floor(float(n) / bitsPerDigit))
    result = BigInt(False)
    arrayCopy(x.digits, 0, result.digits, digitCount,len(result.digits) - digitCount)
    bits = n % bitsPerDigit
    rightBits = bitsPerDigit - bits
    i =len(result.digits) - 1
    i1 = i - 1
    while (i > 0):
        result.digits[i] = ((result.digits[i] << bits) & maxDigitVal) | ((result.digits[i1] & highBitMasks[bits]) >> (rightBits))   #   原为无符号右移>>>
        i -= 1
        i1 -= 1
    result.digits[0] = ((result.digits[i] << bits) & maxDigitVal)
    result.isNeg = x.isNeg
    return result

lowBitMasks = [0x0000, 0x0001, 0x0003, 0x0007, 0x000F, 0x001F,0x003F, 0x007F, 0x00FF, 0x01FF, 0x03FF, 0x07FF, 0x0FFF, 0x1FFF, 0x3FFF, 0x7FFF, 0xFFFF]

def biShiftRight(x, n):
    global bitsPerDigit
    digitCount = int(math.floor(float(n) / bitsPerDigit))
    result = BigInt(False)
    arrayCopy(x.digits, digitCount, result.digits, 0, len(x.digits) - digitCount)
    bits = n % bitsPerDigit
    leftBits = bitsPerDigit - bits
    i = 0
    i1 = i + 1
    while (i < len(result.digits) - 1):
        result.digits[i] = (result.digits[i] >> bits) | ((result.digits[i1] & lowBitMasks[bits]) << leftBits)   #原为无符号右移>>>
        i += 1
        i1 += 1
    result.digits[len(result.digits) - 1] >>= bits  #原为无符号右移>>>
    result.isNeg = x.isNeg
    return result

def biMultiplyByRadixPower(x, n):
    result = BigInt(False)
    arrayCopy(x.digits, 0, result.digits, n, len(result.digits) - n)
    return result

def biDivideByRadixPower(x, n):
    result = BigInt(False)
    arrayCopy(x.digits, n, result.digits, 0, len(result.digits) - n)
    return result

def biModuloByRadixPower(x, n):
    result = BigInt(False)
    arrayCopy(x.digits, 0, result.digits, 0, n)
    return result

def biCompare(x, y):
    if (x.isNeg != y.isNeg):
        if (x.isNeg):
            return 1 - 2 * 1
        else:
            return 1 - 2 * 0
    i = len(x.digits) - 1
    while (i >= 0):
        if (x.digits[i] != y.digits[i]):
            if (x.isNeg):
                if (x.digits[i] > y.digits[i]):
                    return 1 - 2 * 1
                else:
                    return 1 - 2 * 0
            else:
                if (x.digits[i] < y.digits[i]):
                    return 1 - 2 * 1
                else:
                    return 1 - 2 * 0
        i -= 1
    return 0

def biDivideModulo(x, y):
    global bitsPerDigit,biHalfRadix,biRadixSquared,bigOne,biRadix
    nb = biNumBits(x)
    tb = biNumBits(y)
    origYIsNeg = y.isNeg
    
    if (nb < tb):
        #// |x| < |y|
        if (x.isNeg):
            q = biCopy(bigOne)
            q.isNeg =  not y.isNeg
            x.isNeg = False
            y.isNeg = False
            r = biSubtract(y, x)
			#// Restore signs, 'cause they're references.
            x.isNeg = True
            y.isNeg = origYIsNeg
        else:
            q = BigInt(False)
            r = biCopy(x)
        return [q, r]
    
    q = BigInt(False)
    r = x
    
    #// Normalize Y.
    t = int(math.ceil(tb / bitsPerDigit)) - 1
    Lambda = 0
    while (y.digits[t] < biHalfRadix):
        y = biShiftLeft(y, 1)
        Lambda += 1
        tb += 1
        t = int(math.ceil(tb / bitsPerDigit)) - 1
    
    #// Shift r over to keep the quotient constant. We'll shift the
    #// remainder back at the end.
    r = biShiftLeft(r, Lambda)
    nb += Lambda #// Update the bit count for x.
    
    n = int(math.ceil(float(nb) / bitsPerDigit)) - 1   #--Error--#
    
    b = biMultiplyByRadixPower(y, n - t)
    while (biCompare(r, b) != -1):
        q.digits[n - t] += 1
        r = biSubtract(r, b)
    #print "r=",r.digits
    #print "q= ",q.digits
    for i in range(n, t, -1):
        if (i >= len(r.digits)):
            ri = 0
        else:
            ri = r.digits[i]
        if (i - 1 >= len(r.digits)):
            ri1 = 0
        else:
            ri1 = r.digits[i - 1]
        if (i - 2 >= len(r.digits)):
            ri2 = 0
        else:
            ri2 = r.digits[i - 2]
        if (t >= len(y.digits)):
            yt = 0
        else:
            yt = y.digits[t]
        if (t - 1 >= len(y.digits)):
            yt1 = 0
        else:
            yt1 = y.digits[t - 1]
        
        #print "ri= ", ri,"ri1= ", ri1,"ri2= ", ri2
        #print "yt= ", yt,"yt1= ", yt1
        if (ri == yt):
            q.digits[i - t - 1] = maxDigitVal
        else:
            q.digits[i - t - 1] = int(math.floor(float(ri * biRadix + ri1) / yt))

        c1 = q.digits[i - t - 1] * ((yt * biRadix) + yt1)
        c2 = (ri * biRadixSquared) + ((ri1 * biRadix) + ri2)
        #print "q.digits[",i - t - 1,"]= ",q.digits[i - t - 1]
        while (c1 > c2):
            q.digits[i - t - 1] -= 1
            c1 = q.digits[i - t - 1] * ((yt * biRadix) | yt1)
            c2 = (ri * biRadix * biRadix) + ((ri1 * biRadix) + ri2)
        #print "2: q.digits[",i - t - 1,"]= ",q.digits[i - t - 1]
        b = biMultiplyByRadixPower(y, i - t - 1)
        #print "1: r= ",r.digits
        #print biMultiplyDigit(b, q.digits[i - t - 1]).digits
        r = biSubtract(r, biMultiplyDigit(b, q.digits[i - t - 1]))
        #print "2: r= ",r.digits
        
        if (r.isNeg):
            r = biAdd(r, b)
            q.digits[i - t - 1] -= 1
        #print "3: q.digits[",i - t - 1,"]= ",q.digits[i - t - 1]
        #print "3: r= ",r.digits
    
    r = biShiftRight(r, Lambda)
    #// Fiddle with the signs and stuff to make sure that 0 <= r < y.
    q.isNeg = x.isNeg != origYIsNeg
    if (x.isNeg):
        if (origYIsNeg):
            q = biAdd(q, bigOne)
        else:
            q = biSubtract(q, bigOne)
        y = biShiftRight(y, Lambda)
        r = biSubtract(y, r)
    
    #// Check for the unbelievably stupid degenerate case of r == -0.
    if (r.digits[0] == 0 and biHighIndex(r) == 0):
        r.isNeg = False
    
    return [q, r]


def biDivide(x, y):
    return biDivideModulo(x, y)[0]

def biModulo(x, y):
    return biDivideModulo(x, y)[1]

def biMultiplyMod(x, y, m):
    return biModulo(biMultiply(x, y), m)

def biPow(x, y):
    global bigOne
    result = bigOne
    a = x
    while (1) :
        if ((y & 1) != 0):
            result = biMultiply(result, a)
        y >>= 1
        if (y == 0):
            break
        a = biMultiply(a, a)
    return result

def biPowMod(x, y, m):
    global bigOne
    result = bigOne
    a = x
    k = y
    while (1):
        if ((k.digits[0] & 1) != 0):
            result = biMultiplyMod(result, a, m)
        k = biShiftRight(k, 1)
        if (k.digits[0] == 0 and biHighIndex(k) == 0):
            break
        a = biMultiplyMod(a, a, m)
    return result