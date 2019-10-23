'''
Encryption and Digital Fingerprinting

'''
import numpy
import math
import time
import hashlib
import random

def simple(a, b, m):
    a = int(a, 2)
    b = int(b, 2)
    ans = 1

    while b > 0:
        r = b % 2
        b = int(b/2)
        if r == 1:
            ans = a * ans
        if b == 0:
            break
        a = a*a
    return ans % m

# Faster implementation, taking the mod m of a and returning the mod value


def modified(a, b, m):
    a = int(a, 2)
    m = int(m, 2)
    a = a % m
    b = int(b, 2)

    ans = 1
    while b > 0:
        r = b % 2
        b = b//2
        if r == 1:
            ans = (a % m) * (ans % m)
            # Since a*ans mod m = a mod m * ans mod m
        if b == 0:
            break
        # TO AVOID EXTRA a%m * a%m  at the last loop
        a = (a % m)*(a % m)
        # Since a*a mod m = a mod m * a mod m
    return ans % m

# <-----------------------Only for testing ------------------------>
# binaryA = bin(2)
# binaryB = bin(3)
# for i in range(105000, 105010):
#     xStart = time.time()
#     x = simple(bin(i-5000), bin(i), 40302)
#     xEnd = time.time() - xStart
#     print("xEnd: ", xEnd)

#     yStart = time.time()
#     y = modified(bin(i-5000), bin(i), 40302)
#     yEnd = time.time() - yStart
#     print("yEnd: ", yEnd)

#     print("simple calculation : ", x)
#     print("mod calculation : ", y)

#     if x != y:
#         print ("EROROROROROR")
#         break


# <------------------------Problem 4 Part 2 -------------------->
file = open("gallicWars.txt")
public = open("publicKey.txt")
private = open("privateKey.txt")

for line in public:
    publicData = line.split(',')
for line in private:
    privateData = int(line)

publicData = [int(num) for num in publicData]

# publicData stores value in publickey
# privateData stores value in privatekey

# Function that fingerprints the file in hexadecimal


def hashcode(file):
    return hashlib.md5(str(file).encode()).hexdigest()

# Function that encrypts the file with modified function from problem 3


def Encrypt(x, e, N):
    return modified(x, e, N)

# Function that decrypts the file with modified function from problem 3


def Decrypt(x, d, N):
    return modified(x, d, N)


# Encrypt the hashcoded file
encryptedFingerprint = Encrypt(bin(int(hashcode(file), 16)),
                               bin(publicData[1]), bin(publicData[0]))

# Decrypt the encrypted file
decryptedFingerprint = Decrypt(
    bin(encryptedFingerprint), bin(privateData), bin(publicData[0]))

# Compare the hashcoded and decrpyed fingerprint
print("hashcode: ", int(hashcode(file), 16))
print("Encrypted: ", encryptedFingerprint)
print("Decrypted: ", decryptedFingerprint)
