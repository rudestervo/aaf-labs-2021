from functools import *

def sum(a, b) :
    return a + b

AgreggateFunc = {
    'AVG': lambda arr: reduce(sum, arr) / len(arr),
    'MAX': lambda arr: max(arr),
    'COUNT': lambda arr: len(arr),
    'COUNT_DISTINCT': lambda arr: len(set(arr))
}