# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:41:18 2016

@author: lcl
"""
"""
var RSAAPP = {};

RSAAPP.NoPadding = "NoPadding";
RSAAPP.PKCS1Padding = "PKCS1Padding";
RSAAPP.RawEncoding = "RawEncoding";
RSAAPP.NumericEncoding = "NumericEncoding";
"""
from BigInt import *
from Barrett import BarrettMu


class RSAKeyPair:
    e = None
    d = None
    m = None
    chunkSize = None
    radix = None
    barrett = None
    
    def __init__(self,encryptionExponent, decryptionExponent, modulus):
        self.e = biFromHex(encryptionExponent)
        self.d = biFromHex(decryptionExponent)
        self.m = biFromHex(modulus)
        self.chunkSize = 256 / 8#2 * biHighIndex(self.m)
        self.radix = 16
        self.barrett = BarrettMu(self.m)

def encryptedString(key, s):
    
    #*      Plaintext In
    #*      ------------
    #*
    #*      d5 d4 d3 d2 d1 d0
    #*
    #*      OHDave
    #*      ------
    #*
    #*      d5 d4 d3 d2 d1 d0 00 00 00 /.../ 00 00 00 00 00 00 00 00
    
    a = []                             # The usual Alice and Bob stuff
    sl =  len(s)                       # Plaintext string length
    i = 0                              # The usual Fortran index stuff
    j = 0
    k = 0                              
    padtype = 0                       # Type of padding to do--OHDave
    encodingtype = 0                  # Type of output encoding--NumericEncoding
    #rpad  = None                      # Random pad
    al = len(a)                        # Array length
    result = ""                        # Cypthertext result
    block  = None                     # Big integer block to encrypt
    crypt  = None                      # Big integer result
    text  = None                       # Text result
    
    j = key.chunkSize - 1
    while (i < sl):
        if (padtype):
            a.append(ord(s[i]))
        else:
            a.append(ord(s[i]))
        i += 1
        j -= 1

    if (padtype == 1):
        i = 0
    j = key.chunkSize - (sl % key.chunkSize)
    
    while (j > 0):
        a.append(0)
        j -=1

    al = len(a)
    #print "a=",a
    for i in range(0, al, key.chunkSize):
        block = BigInt(False)
        j = 0
        
        k = i
        while (k < i+key.chunkSize):
            block.digits[j] = a[k] + (a[k+1] << 8)
            #print "block.digits[",j,"]= ",block.digits[j]
            k += 2
            j += 1
        #print "block= ",block.digits
        #print "key.e= ",key.e.digits
        crypt = key.barrett.powMod(block, key.e)
        #print "crypt= ",crypt.digits
        if (encodingtype == 1):
            text = biToBytes(crypt)
        else:
            #print "key.radix",key.radix
            if (key.radix == 16):
                text = biToHex(crypt)
            else:
                text = biToString(crypt, key.radix)
        result += text;
    return result;
    

def decryptedString(key, c):
    blocks = c.split(" ")              #// Multiple blocks of cyphertext
    b = None                                 #// The usual Alice and Bob stuff
    i = 0                                #// The usual Fortran index stuff
    j = 0
    bi = None                                #// Cyphertext as a big integer
    result = ""                        #// Plaintext result
    
    for i in range(len(blocks)):
        if (key.radix == 16):
            bi = biFromHex(blocks[i])
        else:
            bi = biFromString(blocks[i], key.radix)
        b = key.barrett.powMod(bi, key.d)
        for j in range(0,biHighIndex(b)+1):
            result += chr(b.digits[j] & 255)
            result += chr(b.digits[j] >> 8)
            #//result += String.fromCharCode(b.digits[j] >> 8,b.digits[j] & 255);
    if (result[-1] == 0):
        result = result[:-1]
    return (result)
"""
password = "1234567812345678"
key = RSAKeyPair("10001","367fbdde3df00db317f914949dd02b01","94b8c162b498f08d139461950b4f3851")
password = encryptedString(key, password)
print "password_encrypted= ",password
password = decryptedString(key,password)
print "password_decrypted= ",password
"""
#--RSA--#
import random


def _aks_(a,n):
    a1 = pow(17-a,n,n)
    a2 = pow(17,n,n) - (a % n)
    if a1 == a2:
        return 1
    else:
        return 0
        
def get_hugeprime():
    flag = 0
    while not flag:
        n = random.randrange(2**8,2**10)
        if (n%2==0 or n%3==0 or n%5==0 or n%7==0 or n%13==0):
            continue
        flag = _aks_(2,n)
    return n

def gcd(a,b):
    temp = a
    if (a < b):
        a = b
        b = temp
    while (b != 0):
        temp = a % b
        a = b
        b = temp
    return (a,b)

def product_e(euler_n):     
	tepflag=1
     	while tepflag:          	
		e=random.randrange(euler_n)
		if (gcd(e,euler_n)==(1,0)):
			tepflag=0
	return e 

def extended_euclid(a,b):
    X1=1
    X2=0
    X3=b
    Y1=0
    Y2=1
    Y3=a
    while (Y3!=1):
        if Y3==0:
            return 0
        Q=X3/Y3
        T1=X1-Q*Y1
        T2=X2-Q*Y2
        T3=X3-Q*Y3
        X1=Y1
        X2=Y2
        X3=Y3
        Y1=T1
        Y2=T2
        Y3=T3
    return Y2%b


def getRSA():
    #-- random prime p and q--#
    p = get_hugeprime()
    q = get_hugeprime()
    while (p == q):
        q = get_hugeprime()
    
    n = p * q
    euler_n = (p-1) * (q - 1) 
    d = 0
    while(d == 0):
        e = product_e(n)
        d = extended_euclid(e,euler_n)
    rsa = {}
    rsa['n'] = n
    rsa['euler_n'] = euler_n
    rsa['e'] = e
    rsa['d'] = d
    return rsa