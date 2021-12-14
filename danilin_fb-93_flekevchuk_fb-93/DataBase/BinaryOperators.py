allBinares = {
    'EQUAL': lambda param1, param2: param1==param2,
    'NOT_EQUAL': lambda param1, param2: param1!=param2,
    'MORE_EQUAL':  lambda param1, param2: param1>=param2,
    'LESS_EQUAL':  lambda param1, param2: param1<=param2,
    'LESS': lambda param1, param2: param1<param2,
    'MORE': lambda param1, param2: param1>param2
}
