from itertools import cycle

def decrypt(data, key):
    # print("type:", type(data), type(key))
    # print("bin", bin(data), bin(key))
    beforeXOR = "{0:b}".format(data ^ key)
    if(len(beforeXOR)<9):
        beforeXOR = "0"*(8-len(beforeXOR)) + beforeXOR
    # print("beforeXOR:", beforeXOR)

    beforeRotate = beforeXOR[-5:] + beforeXOR[:-5]
    # print("beforeRotate:", beforeRotate)
    return beforeRotate


# with open(r"E:\0_Work\1_repositories\ASU_CSE545\Unit2_Assignment\sf.txt.gz", "rb" ) as f:
#     # open file in binary
#     data = f.read()
#     print(type(data))
#     print(bin(data[9]))

#     # print(bin(10292021))
#     # print(int("00101101", 2))
#     print(chr(int("00101110", 2)))

#     "00110011" # data[9] = 
#     keys = "SECRETPASS"
#     nums = "123"
#     for key, num in zip(keys, cycle(nums)):
#         print(key, num)

#     print(len("SECRETPASS"))

def main():
    keys = "SECRETPASS"
    print(len("secretfile.txt"))
    with open(r"E:\0_Work\1_repositories\ASU_CSE545\Unit2_Assignment\sf.txt.gz", "rb" ) as f:
        new_file_byte_array = []
        filename = ""
        data = f.read()
        print("data: ", data, data[0])
        # data = data[10:24]
        # print(data[10])
        # print(bin(data[10]))
        for chrKey, decInt in zip(cycle(keys),data):
            # print("for:", chrKey, decInt)
            decIntKey = ord(chrKey)
            plaintext = decrypt(decInt, decIntKey)
            print("plaintext:", plaintext, "=", chr(int(plaintext, 2)))
            # print(int(plaintext, 2))
            new_file_byte_array.append(int(plaintext, 2))
            filename = filename + chr(int(plaintext, 2))
        some_bytes = bytearray(new_file_byte_array)
        print(filename)
        with open (r"E:\0_Work\1_repositories\ASU_CSE545\Unit2_Assignment\nsf.txt.gz", "wb") as nf:
            nf.write(bytes(some_bytes))


        # plaintext = decrypt(data[10], 0b01010011)
        # print("plaintext:", plaintext, "=", chr(int(plaintext, 2)) )

    

if __name__ == "__main__":
    main()
