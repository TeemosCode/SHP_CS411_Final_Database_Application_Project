# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:41:18 2016

@author: lcl
"""
from BigInt import *

class BarrettMu:
    modulus = None
    k = None
    mu = None
    bkplus1 = None
    
    def __init__(self,m):
        self.modulus = biCopy(m)
        self.k = biHighIndex(self.modulus) + 1
        b2k = BigInt(False)
        b2k.digits[2 * self.k] = 1 # // b2k = b^(2k)
        #print "b2k= ",b2k.digits,"modulus= ",self.modulus.digits
        self.mu = biDivide(b2k, self.modulus)    #--Error--#
        self.bkplus1 = BigInt(False)
        self.bkplus1.digits[self.k + 1] = 1 # // bkplus1 = b^(k+1)
    def modulo(self, x):
        q1 = biDivideByRadixPower(x, self.k - 1)
        q2 = biMultiply(q1, self.mu)
        q3 = biDivideByRadixPower(q2, self.k + 1)
        r1 = biModuloByRadixPower(x, self.k + 1)
        r2term = biMultiply(q3, self.modulus)
        r2 = biModuloByRadixPower(r2term, self.k + 1)
        r = biSubtract(r1, r2)
        if (r.isNeg) :
            r = biAdd(r, self.bkplus1)
        if (biCompare(r, self.modulus) >= 0):
            rgtem = True
        else:
            rgtem = False
        while (rgtem):
            r = biSubtract(r, self.modulus)
            if (biCompare(r, self.modulus) >= 0):
                rgtem = True
            else:
                rgtem = False
        return r
    
    def multiplyMod(self, x, y):
        xy = biMultiply(x, y)
        #print "xy= ", xy.digits
        return self.modulo(xy)
    
    def powMod(self, x, y):
        result = BigInt(False)
        result.digits[0] = 1
        a = x
        k = y
        
        while (1):
            if ((k.digits[0] & 1) != 0):
                result = self.multiplyMod(result, a)
                #print "result = ",result.digits
            k = biShiftRight(k, 1)
            #print "test"
            if (k.digits[0] == 0 and biHighIndex(k) == 0):
                break
            a = self.multiplyMod(a, a) 
            #print "k.digits[0]=",k.digits[0],"biHighIndex(k)=",biHighIndex(k)
        return result