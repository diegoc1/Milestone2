'''
Channel coding module for transmitter and receiver
'''

import numpy as np
import collections

from random import randrange
import hamming_db   # Matrices for Hamming codes

''' Transmitter side ---------------------------------------------------
'''
def get_frame(databits, cc_len):
    '''
    Perform channel coding to <databits> with Hamming code of n=<cc_len>
    Add header and also apply Hamming code of n=3
    Return the resulted frame (channel-coded header and databits)
    '''

    n, k, index, G = hamming_db.gen_lookup(cc_len)


    
    header = get_header(databits, index)

    i, payload = encode(databits, cc_len)
    i, encoded_header = encode(header, 3)
    frame = np.append(encoded_header ,payload)
    
    return frame
    

#Input: integer
#Output: A bit array of length 16 for that integer (that means the max input integer is 2^17 - 1)
def int_to_16_bit_array(inputInt):
    bit_string = np.binary_repr(inputInt)
    bit_array = [int(char) for char in bit_string]
    if len(bit_array) < 16:
        for i in range(16 - len(bit_array)):
            bit_array.insert(0, 0)
    return bit_array

def get_header(payload, index):
    '''
    Construct and return header for channel coding information.
    Do not confuse this with header from source module.
    Communication system use layers and attach nested headers from each layers 
    '''

    num_bits = len(payload)
    num_bits_bit_array = int_to_16_bit_array(num_bits)

    index_bit_array = int_to_16_bit_array(index)

    header = num_bits_bit_array + index_bit_array


    return header
    
def encode(databits, cc_len):
    '''
    Perfrom channel coding to <databits> with Hamming code of n=<cc_len>
    Pad zeros to the databits if needed.
    Return the index of our used code and the channel-coded databits
    '''


    n, k, index, G = hamming_db.gen_lookup(cc_len)

    G_r = np.matrix(np.reshape(G, (k, n)))

    encoded_bits = np.array([]).astype(np.uint8)
    c = 0
    while c <= len(databits) - k:
        bits_to_encode = np.matrix(databits[c:c+k])
        codeword = bits_to_encode * G_r
        codeword = codeword % 2
        encoded_bits = np.append(encoded_bits, codeword)
        c += k

    if c != len(databits):
        bits_to_encode = databits[c:]
        while len(bits_to_encode) < k:
            bits_to_encode = np.append(bits_to_encode, 0)
        bits_to_encode = np.matrix(bits_to_encode)
        codeword = bits_to_encode * G_r
        codeword = codeword % 2
        encoded_bits = np.append(encoded_bits, codeword)
    return index, encoded_bits

''' Receiver side ---------------------------------------------------
'''    


def getIntFromBinaryArr(numpyArr):
        numpyArr = numpyArr.astype(int)
        bit_array = numpyArr.tolist()
        bit_string = ''.join(str(bin_num) for bin_num in bit_array)
        return int(bit_string, 2)

def get_databits(recd_bits):
    '''
    Return channel-decoded data bits
    Parse the header and perform channel decoding.
    Note that header is also channel-coded    
    '''

    n, k, index, G = hamming_db.gen_lookup(3)
   # import pdb; pdb.set_trace()

   #Multiply by 3 becasue of encoding
    header = recd_bits[0:32*3]

    header = decode(header, index)

    num_bits_to_decode_array = header[0:16]
    index_for_payload_array = header[16:32]



    num_bits_to_decode = getIntFromBinaryArr(num_bits_to_decode_array)
    index_for_payload = getIntFromBinaryArr(index_for_payload_array)

    print "num_bits_to_decode", num_bits_to_decode

    payload = recd_bits[32*3:]
    databits = decode(payload, index_for_payload)

    return databits[:num_bits_to_decode]


def getErrorIndex(output, H, n, k):
    output = np.transpose(output)
    output = output.tolist()
    output = output[0]

    for i in range(n):
        col = H[:, i]
        col = col.tolist()
        if listsEqual(col, output):
            return i
    return -1

def listsEqual(a, b, show = False):
    if len(a) != len(b):
        if show:
            "DIFF LENGTHS"
        return False

    for i in range(len(a)):
        if a[i] != b[i]:
            if show:
                print "error at ", i
            return False
    return True

def decode(coded_bits, index):
    '''
    Decode <coded_bits> with Hamming code which corresponds to <index>
    Return decoded bits
    '''
    n, k, H = hamming_db.parity_lookup(index)

    ind = 0
    decoded_bits = np.array([]).astype(np.uint8)
    while(ind < len(coded_bits)):
        bits_to_decode = coded_bits[ind: ind + n]
        bits = (np.matrix(bits_to_decode))
        data_bits = (H * np.transpose(bits)) % 2
        error_ind = getErrorIndex(data_bits, H, n, k)
        if (error_ind != -1):
            print "correcting error at ", ind + error_ind + 96
            print "changing ", bits_to_decode[n-k:]
            bits_to_decode[error_ind] = (bits_to_decode[error_ind] + 1) % 2
            print "it is now ", bits_to_decode[n-k:]
            print
        decoded_bits = np.append(decoded_bits, bits_to_decode[n-k:])
        ind = ind + n
    return decoded_bits



# f = get_frame([0, 1, 1, 0, 1, 1 , 1, 0, 1, 1, 0], 7)

for x in range(200):
    length = randrange(10000)

    l = [0] * length

    for i in range(length):
        c = randrange(2)
        if c == 1:
            l[i] = 1

    print "size of array", length


    f = get_frame(l, 15)

    s = f.shape[0]
    ind = randrange(s)


    f[ind] = ( f[ind] + 1 ) % 2


    k = get_databits(f)
    print "original: ", l
    print " new: ", k
    print "ind is ", ind
    print "length is ", len(k)

    if listsEqual(l, k, True):
        print "LISTS EQUAL"
    else:
        exit()

# exit()
# i, a = encode([0, 1, 1, 0, 1, 1 ,1,1], 7)
# print "encoded", a
# print "Asdf"


# print decode(a, i)
