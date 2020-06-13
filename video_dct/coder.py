import math

from rs.irreducible_polynomials import irreducible_polynomials
from rs.galois_fields import ExtendedGaloisField
from rs.polinomials import Polynomials
from rs.reed_solomon import RS_Extended


class CoderDecoder:
    def __init__(self):
        self.b = 1
        self.m = 8
        self.n = pow(2, self.m) - 1
        self.k = self.n // 2 + 1
        self.d = self.n - self.k + 1
        self.t = (self.d - 1) // 2
        self.rs = self.initialize_rs_generator()[0]
        self.generator = self.initialize_rs_generator()[1]
        self.message_sequence = []
        self.rest_of_message = []

    @staticmethod
    def message_seq_to_bin_str(message):
        bin_message = ''.join(format(x, 'b').zfill(8) for x in message)
        return bin_message

    @staticmethod
    def bin_str_to_msg_seq(message):
        msg_seq = []
        for i in range(0, len(message), 8):
            temp_data = int(message[i:i + 8], 2)
            msg_seq.append(temp_data)
        return msg_seq

    def check_seq_size(self, num_msg_seq):

        if len(num_msg_seq) > self.k:
            self.rest_of_message = num_msg_seq[self.k:]
            self.message_sequence = num_msg_seq[:self.k]
        elif len(num_msg_seq) < self.k:
            self.message_sequence = num_msg_seq + [0] * (self.k - len(num_msg_seq))
            self.rest_of_message = []

        return num_msg_seq

    def initialize_rs_generator(self):
        # generate field
        primitive_poly = irreducible_polynomials.get(self.m)
        gf = ExtendedGaloisField(prime_order=2, n=self.n, primitive_poly=primitive_poly)

        # generate root list
        roots = []
        for i in range(self.b, self.b + self.d - 1):
            roots.append(gf.exp_bin[i])

        poly = Polynomials(gf=gf)
        rs = RS_Extended(n=self.n, k=self.k, d=self.d, gf=gf, polynomial=poly, roots=roots)

        # calculate min poly
        generator = rs.generator_poly()
        result, check_g = rs.check_poly(generator)

        return rs, generator

    def encode_message(self, message_sequence):
        self.check_seq_size(num_msg_seq=message_sequence)

        # encode message
        c_x = self.rs.coder(info_sequence=self.message_sequence, generator=self.generator)

        return c_x

    def decode_message(self, message_sequence):

        decoded_message = self.rs.decoder(message=message_sequence, b=self.b, t=self.t)
        decoded_message = decoded_message[-self.k:]

        while decoded_message[-1] == 0:
            decoded_message.pop()

        return decoded_message



class Converter:

    @staticmethod
    def bin_to_str(message):
        str_data = ''
        for i in range(0, len(message), 8):
            temp_data = int(message[i:i + 8], 2)
            str_data += chr(temp_data)
        return str_data

    @staticmethod
    def str_to_bin(message):
        result = ''.join(format(ord(x), 'b').zfill(8) for x in message)
        return result
