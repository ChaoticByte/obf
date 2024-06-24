# Copyright (c) 2024 Julian Müller (ChaoticByte)
# License: MIT

from multiprocessing import Pool


CHUNKSIZE = 1024 * 4


def _obf(args) -> bytearray:
    data_chunk, key, decrypt, iterations = args
    l_data = len(data_chunk)
    l_key = len(key)
    for _ in range(iterations):
        # shift (encrypt)
        if not decrypt:
            for i in range(l_data):
                n = key[i % l_key]
                data_chunk[i] = (data_chunk[i] + n) % 256
        # transpose
        # list of tuples that stores transposition data (from, to):
        tp = [] # (this is extremely memory inefficient for large chunksizes)
        k = 0
        for i in range(l_data):
            k += i + key[i % l_key]     # we add to k
            j = k % l_data              # and use k here (more obfuscation)
            tp.append((i, j)) # store transposition data
        if decrypt:
            tp.reverse()
        for a, b in tp:
            # swap values
            data_chunk[a], data_chunk[b] = data_chunk[b], data_chunk[a]
        # unshift (decrypt)
        if decrypt:
            for i in range(l_data):
                n = key[i % l_key]
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
    # split into chunks
    chunks = []
    p = 0
    while p < len(data):
        p_new = p + CHUNKSIZE
        chunk = data[p:p_new]
        chunks.append((chunk, key, decrypt, iterations))
        p = p_new
    # don't need that anymore
    del data
    # create mp pool and process
    pool = Pool(processes=4)
    results = pool.map(_obf, chunks)
    # don't need that anymore
    del chunks
    # done
    return bytes(b''.join(results))
