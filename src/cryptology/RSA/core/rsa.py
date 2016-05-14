import time
import random

prime_in_1000 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
                 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317,
                 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443,
                 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
                 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701,
                 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
                 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983,
                 991, 997]


def gcd(a, b):
    x, y = a, b
    flag = 1
    while y != 0:
        if x < y:
            x, y = y, x
        if x % 2 == 0 and y % 2 == 0:
            flag *= 2
            x, y = x//2, y//2
        elif x % 2 == 0:
            x //= 2
        elif y % 2 == 0:
            y //= 2
        else:
            x, y = (x+y)//2, (x-y)//2
    return x * flag


def power_mod(base, e, m):
    result = 1
    b = base
    b %= m
    while e > 0:
        if e & 1 == 1:
            result = result * b % m
        e >>= 1
        b = b**2 % m
    return result


def prime_test(n, test=(2, 3, 5, 13, 127, 499)):
    for m in prime_in_1000:
        if n % m == 0 and n not in prime_in_1000:
            return False
    for m in test:
        if power_mod(m, n-1, n) == 1:
            pass
        else:
            return False
    return True


def prime_num_produce():
    random.seed(time.time())
    prime_num = set([])
    while len(prime_num) != 2:
        n = random.randint(2**511, 2**512)
        if n % 2 == 0:
            n += 1
        if prime_test(n) is True:
            prime_num.add(n)
    return prime_num


def produce_e(n=None):
    random.seed(time.time())
    while True:
        e = random.randint(3, n-1)
        if gcd(e, n) == 1:
            return e


def extended_euclid(a, b):
    x1 = 1
    x2 = 0
    x3 = b
    y1 = 0
    y2 = 1
    y3 = a
    while y3 != 1:
        if y3 == 0:
            return 0
        q = x3 // y3
        t1 = x1 - q * y1
        t2 = x2 - q * y2
        t3 = x3 - q * y3
        x1 = y1
        x2 = y2
        x3 = y3
        y1 = t1
        y2 = t2
        y3 = t3
    return y2 % b


def key_generator():
    rsa_p, rsa_q = prime_num_produce()
    rsa_n = rsa_q * rsa_p
    phi_n = (rsa_p-1) * (rsa_q-1)
    rsa_e = produce_e(phi_n)
    rsa_d = extended_euclid(rsa_e, phi_n)
    return {'P': [rsa_e, rsa_n], 'S': [rsa_d, rsa_n]}


def encryption(message, e, n):
    return map(lambda x: power_mod(x, e, n), message)


def decryption(c, d, n):
    return map(lambda x: power_mod(x, d, n), c)


def text_to_ascii(text):
    tmp = []
    for ch in text:
        tmp.append(ord(ch))
    return tmp
