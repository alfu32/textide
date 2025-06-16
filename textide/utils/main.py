def divide_list(arr: list, by: int,chunk_size:int) -> (list, list, list):
    l = len(arr)
    if chunk_size >= l:
        return [],arr,[]

    before = []
    visible = []
    after = []
    chunk_id, chunk_pos = divmod(by, chunk_size)
    before = arr[0:chunk_id * chunk_size]
    visible = arr[chunk_id * chunk_size:(chunk_id + 1) * chunk_size]
    after = arr[(chunk_id + 1) * chunk_size:]
    if 0 == (chunk_id * chunk_size):
        before = []
    if l == ((chunk_id + 1) * chunk_size):
        visible = visible + after
        after = []
    return before, visible, after