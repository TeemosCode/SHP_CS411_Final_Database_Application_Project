#from django.test import TestCase

# Create your tests here.
class temp:
    x = None
    y = None
    z = None
    
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
t = temp(1,2,3)
print t.x