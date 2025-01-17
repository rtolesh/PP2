#Example Python Numbers:
x = 3    #int
y = 2.8  #float
z = 1j   #complex


#Integers:
a = 2
b = 613286387126387618
c = -61616161
print(type(a))
print(type(b))
print(type(c))

#Float:
d = 2.26
e = 1.0
f = -64.35
print(type(d))
print(type(e))
print(type(f))

#Complex:
g = 3+5j
h = 5j
k = -5j
print(type(g))
print(type(h))
print(type(k))

#Convert from one type to another:
x = 1    
y = 2.8  
z = 1j   

#convert from int to float:
a = float(x)

#convert from float to int:
b = int(y)

#convert from int to complex:
c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))

# Random number:
import random
print(random.randrange(1, 21))