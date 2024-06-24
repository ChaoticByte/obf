# Copyright (c) 2024 Julian Müller (ChaoticByte)
# License: MIT

from multiprocessing import Pool

CHUNKSIZE = 1024 * 4


def _obf(args) -> bytearray:
    data_chunk, key, decrypt, iterations = args
    len_data = len(data_chunk)
    len_key = len(key)
    for _ in range(iterations):
        # shift (encrypt)
        if not decrypt:
            for i in range(len_data):
                n = key[i % len_key]
                data_chunk[i] = (data_chunk[i] + n) % 256
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
            a_ = data_chunk[a]
            b_ = data_chunk[b]
            data_chunk[a] = b_
            data_chunk[b] = a_
        # unshift (decrypt)
        if decrypt:
            for i in range(len_data):
                n = key[i % len_key]
                b = data_chunk[i] - n
                while b < 0:
                    b = 256 + b
                data_chunk[i] = b
    return data_chunk


def obf(data: bytes, key: bytes, decrypt: bool = False, iterations: int = 8, processes: int = 4) -> bytes:
    assert type(data) == bytes
    assert type(key) == bytes
    assert type(iterations) == int
    assert type(decrypt) == bool
    assert type(processes) == int
    data = bytearray(data)
    key = bytearray(key)
    len_data_complete = len(data)

    chunks = []
    p = 0
    while p < len_data_complete:
        p_new = p + CHUNKSIZE
        chunk = data[p:p_new]
        chunks.append((chunk, key, decrypt, iterations))
        p = p_new

    del data

    pool = Pool(processes=4)
    results = pool.map(_obf, chunks)

    del chunks

    return bytes(b''.join(results))
