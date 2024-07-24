#Student name: Zaid Khan
#Assignment #: 1

def twosCompliment(binary):
    twos = ""
    addOne = True
    temp = ""
    temp2 = ""
    for i in range(len(binary) - 1, -1, -1):
        temp += binary[i]
    for i in range(len(temp)):
        if addOne:
            if temp[i] == '0':
                temp2 += '0'
            else:
                temp2 += '1'
                addOne = False
        else:
            if temp[i] == '1':
                temp2 += '0'
            else:
                temp2 += '1'
    
    for j in range(len(temp2) - 1, -1, -1):
        twos += temp2[j]
    return twos

x = input("give me a binary string to find the twos compliment of: ")
print("The twos compliment of " + x + " is " + twosCompliment(x))
