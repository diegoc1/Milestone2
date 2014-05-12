'''
Channel coding module for transmitter and receiver
'''

import numpy as np

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
    print "n", n
    print "k", k
    print "index", index
    print "G", G

    '''
    header = get_header(databits, index)
    payload = encode(databits)
    frame = encode(header) + payload
    '''
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

    bits_to_encode = databits
    while len(bits_to_encode) < k:
        bits_to_encode = np.append(bits_to_encode, 0)


    bits = (np.matrix(bits_to_encode))

    G_r = np.matrix(np.reshape(G, (k, n)))

    coded_bits = bits * G_r
    
    return index, coded_bits

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

    header = recd_bits[0:32]
    header = decode(header, index)

    num_bits_to_decode_array = header[0:16]
    index_for_payload_array = header[16:32]

    num_bits_to_decode = getIntFromBinaryArr(num_bits_to_decode_array)
    index_for_payload = getIntFromBinaryArr(index_for_payload_array)


    payload = recd_bits[32:]
    databits = decode(payload, index_for_payload)





    return databits

def decode(coded_bits, index):
    '''
    Decode <coded_bits> with Hamming code which corresponds to <index>
    Return decoded bits
    '''
    n, k, H = hamming_db.parity_lookup(index)
    ind = 0
    decoded_bits = np.array()
    while(ind < len(coded_bits)):
        bits_to_decode = coded_bits[ind: ind + n]
        bits = (np.matrix(bits_to_decode))
        data_bits = np.multiply(bits, H)
        decoded_bits += data_bits
        ind = ind + n

    return decoded_bits

print encode([0, 1], 7)
