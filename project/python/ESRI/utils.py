"""
file: utils.py

include lots of utility functions

author: Xueman Mou
date: 2018/4/23
version: 1.0.1
modified: 2018/4/23 14:20:00 GMT +0800

developing env: python 3.5.2
"""

"""
# integer to binary string
"""
def int2bin(d):
	result = []
	if d == 0:
		result.append('0')
	else:
		while(d):
			result.append(d % 2)
			d = d / 2
		result.reverse()
	result = ''.join([str(b) for b in result])
	return result

"""
# binary string to integer
"""
def bin2int(b):
	result = 0
	cnt = 0
	while(cnt < len(b)):
		result += 2**cnt * int(b[len(b) - 1 - cnt])
		cnt += 1
	return result

"""
# left fill binary string to specified length
"""
def bin2fixed_length(b, length):
	result = '';
	if len(b) > length:
		raise RuntimeError('Specified length is shorter than original binary length')
	elif len(b) == length:
		result = b
	else:
		zero_cnt = length - len(b)
		result = '0'*zero_cnt + b
	return result

"""
# Moron code generator
"""
def morton(x, y):
	result = []
	cnt = 0
	if len(x) == len(y):
		while cnt < len(x):
			result.append(y[cnt])
			result.append(x[cnt])
			cnt += 1

	elif len(x) > len(y):
		if len(y) == 31 and len(x) == 32:
			result.append(x[31])
			while cnt < len(y):
				result.append(y[cnt])
				result.append(x[cnt])
				cnt += 1
		else:
			y_cpy = bin2fixed_length(y, len(x))
			while cnt < len(x):
				result.append(y_cpy[cnt])
				result.append(x[cnt])
				cnt += 1

	elif len(x) < len(y):
		x_cpy = bin2fixed_length(x, len(y))
		print(x_cpy)
		print(y)
		while cnt < len(y):
			result.append(y[cnt])
			result.append(x_cpy[cnt])
			cnt += 1

	result = ''.join([str(b) for b in result])
	return result

def main():
	int2bin(0)
	int2bin(1)
	int2bin(2)
	int2bin(3)
	int2bin(4)
	int2bin(5)
	int2bin(6)
	int2bin(7)
	int2bin(8)
	int2bin(27374451)
	int2bin(582901293)

	bin2int('0')
	bin2int('01')
	bin2int('10')
	bin2int('11')
	bin2int('100')
	bin2int('101')
	bin2int('110')
	bin2int('111')
	bin2int('1000')
	bin2int('1101000011011001101110011')
	bin2int('100010101111100101111000101101')

	bin2fixed_length('0', 2)
	bin2fixed_length('01', 4)
	bin2fixed_length('1000', 6)
	bin2fixed_length('1101000011011001101110011', 32)
	bin2fixed_length('100010101111100101111000101101', 31)

	morton('1101000011011001101110011', '100010101111100101111000101101')

if __name__ == '__main__':
	main()