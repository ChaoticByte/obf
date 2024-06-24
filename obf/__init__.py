# Copyright (c) 2024 Julian Müller (ChaoticByte)
# License: MIT

def obf(data: bytes, key: bytes, decrypt: bool = False, iterations: int = 8) -> bytes:
    assert type(data) == bytes
    assert type(key) == bytes
    assert type(iterations) == int
    assert type(decrypt) == bool
    data = bytearray(data)
    key = bytearray(key)
    len_data = len(data)
    len_key = len(key)
    for _ in range(iterations):
        # shift (encrypt)
        if not decrypt:
            for i in range(len_data):
                n = key[i % len_key]
                data[i] = (data[i] + n) % 256
        # transpose
        # list of tuples that stores transposition data (from, to):
        swap_indices = [] # (this is extremely memory inefficient lol)
        k = 0
        for i in range(len_data):
            k += i + key[i % len_key] # we add to k
            j = k % len_data          # and use it to make cryptanalysis harder (I think?)
            swap_indices.append((i, j)) # store transposition data
        if decrypt:
            swap_indices.reverse()
        for a, b in swap_indices:
            # swap values
            a_ = data[a]
            b_ = data[b]
            data[a] = b_
            data[b] = a_
        # unshift (decrypt)
        if decrypt:
            for i in range(len_data):
                n = key[i % len_key]
                b = data[i] - n
                while b < 0:
                    b = 256 + b
                data[i] = b
    return bytes(data)
