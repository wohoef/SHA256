import time
from numpy import sqrt, cbrt

def SHR(x, n):
	if len(x) < n:
		return "0"*len(x)
	else:
		return "0" * n + x[:len(x)-n]

def ROTR(x,n):
	# If n > 2x, for some reason the program will just make n = 2x
	return x[len(x)-n:] + x[:len(x)-n]

def XOR(x,y,z):
	res = int(x,base=2) ^ int(y,base=2) ^ int(z,base=2)
	res = "{0:b}".format(res)
	if len(res) < 32:
		res = "0"*(32-len(res)) + res
	return res

def add(*args):
	res = 0
	for arg in args:
		res += int(arg,base=2)

	res %= 2**32
	res = "{0:b}".format(res)
	if len(res) < 32:
		res = "0"*(32-len(res)) + res
	return res

def choice(x,y,z):
	res = ""
	for xi, yi, zi in zip(x,y,z):
		if int(xi):
			res += yi
		else:
			res += zi

	return res

def majority(x,y,z):
	res = ""
	for xi, yi, zi in zip(x,y,z):
		temp = xi + yi + zi
		if temp.count("1") > 1:
			res += "1"
		else:
			res += "0"
	return res

def sigma0(x):
	x1 = ROTR(x,7)
	x2 = ROTR(x,18)
	x3 = SHR(x,3)
	return XOR(x1,x2,x3)

def sigma1(x):
	x1 = ROTR(x,17)
	x2 = ROTR(x,19)
	x3 = SHR(x,10)
	return XOR(x1,x2,x3)

def usigma0(x):
	x1 = ROTR(x,2)
	x2 = ROTR(x,13)
	x3 = ROTR(x,22)
	return XOR(x1,x2,x3)

def usigma1(x):
	x1 = ROTR(x,6)
	x2 = ROTR(x,11)
	x3 = ROTR(x,25)
	return XOR(x1,x2,x3)

def toBinary(s):
	res = ""
	for i in s:
		b = str(bin(ord(i))[2::])
		if len(b)<8:
			b = "0"*(8-len(b))+b
		res += b

	return res


constants = []
primes = []

for num in range(312):
	if num > 1:
		for i in range(2, num):
			if (num % i) == 0:
				break
		else:
			primes.append(num)

for prime in primes:
	constant = int(prime**(1/3) %1 * (2**32))

	constant = "{0:b}".format(constant)
	if len(constant) < 32:
		constant = "0"*(32-len(constant)) + constant
	constants.append(constant)

def padding(m):
	size = len(m)
	m += "1"
	m += "0" * (448-size-1)
	#The -1 is bc 1 line ago we added one to seperate the message from the padding
	size = "{0:b}".format(size)

	if len(size) < 64:
		size = "0"*(64-len(size)) + size
	m += size

	return m
def compress(initial_values, words):
	compression = initial_values.copy()

	for word, constant in zip(words,constants):
		temp1 = add(usigma1(compression[4]),
					choice(compression[4],compression[5],compression[6]),
					compression[7],
					word,
					constant)
		temp2 = add(usigma0(compression[0]),
					majority(compression[0],compression[1],compression[2]))


		compression.pop(len(compression)-1)
		compression.insert(0,add(temp1,temp2))
		compression[4] = add(compression[4],temp1)
	
	for i in range(len(compression)):
		compression[i] = add(compression[i],initial_values[i])
	return compression

def SHA256(m):
	m = toBinary(m)
	m = padding(m)

	words = []
	for i in range(16):
		i *= 32
		temp = ""
		for ii in range(i, i+32):
			temp += m[ii]
		words.append(temp)
	
	while len(words) < 64:
		i = len(words)
		next_word = add(sigma1(words[i-2]),
						words[i-7],
						sigma0(words[i-15]),
						words[i-16],
						)
		
		words.append(next_word)

	compression = []
	initial_values = []
	for i in range(8):
		prime = primes[i]
		constant = int(prime**(1/2) %1 * (2**32))

		constant = "{0:b}".format(constant)
		if len(constant) < 32:
			constant = "0"*(32-len(constant)) + constant
		initial_values.append(constant)
		compression.append(constant)


	compression = compress(initial_values,words)

	res = ""
	for word in compression:
		word = "{0:x}".format(int(word,base=2))
		res += word

	return res

my_string = input("What string would you like to pass through SHA256? ")
w = SHA256(my_string)
print("OUTPUT: " + w)






