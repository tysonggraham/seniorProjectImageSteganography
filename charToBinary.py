nb = input('Type a String and Press enter: \n')

for ch in nb:
    d = ord(ch)
    b = bin(d)
    print(ch, d, b)