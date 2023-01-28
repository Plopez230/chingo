
import math

def split_columns(lst):
    chunk1 = math.ceil(len(lst)/3)
    remainder = len(lst)-chunk1
    chunk2 = chunk1+math.ceil(remainder/2)
    return [
        lst[0:chunk1],
        lst[chunk1:chunk2],
        lst[chunk2:],
        ]