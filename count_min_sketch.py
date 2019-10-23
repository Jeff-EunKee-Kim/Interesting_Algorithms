'''
Count Min sketch

'''

#* Read Message
file = open("data.txt", "r")
messageString = file.readline()
message = ("".join(messageString)).split(", ")


#* Takes hex string and return first 3 hash indexes
def returnThreeHash(encoding):
    hash1 = int(encoding[0:2], 16)
    hash2 = int(encoding[2:4], 16)
    hash3 = int(encoding[4:6], 16)
    return hash1, hash2, hash3


#* Hashcodes the letter
def hashcode(letter):
    return hashlib.md5(str(letter).encode()).hexdigest()


#* Base count min sketch
def countMinSketch(message):
    table = np.zeros((3, 256), int)

    hitterCount = float(len(message) * 0.01)
    heavyHitter = set()

    for i in message:
        i = int(i)
        hashedMessage = hashcode(i)
        hashIndex = returnThreeHash(hashedMessage)

        minFrequency = 9999999999
        for j in range(3):
            table[j][hashIndex[j]] += 1
            if minFrequency > table[j][hashIndex[j]]:
                minFrequency = table[j][hashIndex[j]]
        if minFrequency >= hitterCount:
            heavyHitter.add(i)

    print("heavyHitter in regular: ", sorted(heavyHitter))
    print(len(heavyHitter))

    return "Made table"


# * Conservative count min sketch
def conservativeCountMinSketch(message):
    table = np.zeros((3, 256), int)
    hitterCount = float(len(message) * 0.01)
    heavyHitter = set()

    for i in message:
        i = int(i)
        hashedMessage = hashcode(i)
        hashIndex = returnThreeHash(hashedMessage)

        minFrequency = 9999999999

        for j in range(3):
            temp = table[j][hashIndex[j]]
            if minFrequency > temp:
                minFrequency = temp

        for j in range(3):
            temp = table[j][hashIndex[j]]
            if minFrequency == temp:
                table[j][hashIndex[j]] += 1

        if minFrequency >= hitterCount:
            heavyHitter.add(i)

    print('heavyHitter for conservative: ', sorted(heavyHitter))
    print(len(heavyHitter))
    return "Made conservative table"


# ! Print heavy hitters for forward stream
countMinSketch(message)
conservativeCountMinSketch(message)

# ! Print heavy hitters for reverse stream
message.reverse()

countMinSketch(message)
conservativeCountMinSketch(message)

# ! Print heavy hitters for uniform random stream
random.shuffle(message)

countMinSketch(message)
conservativeCountMinSketch(message)
