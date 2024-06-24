# Copyright (c) 2024 Julian Müller (ChaoticByte)
# License: MIT

def obf(data: bytes, key: bytes, decrypt: bool = False, iterations: int = 64) -> bytes:
    assert type(data) == bytes
    assert type(key) == bytes
    assert type(iterations) == int
    assert type(decrypt) == bool
    data = bytearray(data)
    key = bytearray(key)
    len_data = len(data)
    len_key = len(key)
    def a(d):
        # shift (encrypt)
        if not decrypt:
            for i in range(len_data):
                n = key[i % len_key]
                d[i] = (d[i] + n) % 256
        # transpose
        swap_indices = [] # list of tuples that stores transposition data (from, to)
        k = 0
        for i in range(len_data):
            k += i + key[i % len_key] # we add to k
            j = k % len_data          # and use it to make cryptanalysis harder (I think?)
            swap_indices.append((i, j)) # store transposition data
        if decrypt:
            swap_indices.reverse()
        for a, b in swap_indices:
            # swap values
            a_ = d[a]
            b_ = d[b]
            d[a] = b_
            d[b] = a_
        # unshift (decrypt)
        if decrypt:
            for i in range(len_data):
                n = key[i % len_key]
                b = d[i] - n
                while b < 0:
                    b = 256 + b
                d[i] = b
        return d
    for i in range(iterations):
        data = a(data)
    return bytes(data)
