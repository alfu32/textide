def divide_list(arr: list, by: int,chunk_size:int) -> (list, list, list):
    l = len(arr)
    if chunk_size > l:
        return [],arr,[]
    before = []
    visible = []
    after = []
    chunk, pos = divmod(by, chunk_size)
    before = arr[0:chunk * chunk_size]
    visible = arr[chunk * chunk_size:(chunk + 1) * chunk_size]
    after = arr[(chunk + 1) * chunk_size:]
    if 0 == (chunk * chunk_size):
        before = []
    if l == ((chunk + 1) * chunk_size):
        after = []
    return before, visible, after